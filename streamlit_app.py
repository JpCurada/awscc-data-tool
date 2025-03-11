import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
import helpers as h
import visualizations as viz

pd.set_option('future.no_silent_downcasting', True)

# Add fragment for the data editor
@st.fragment
def editable_dataframe(df, editor_key):
    edited_df = st.data_editor(
        df.copy(), 
        hide_index=False,
        key=editor_key,
        use_container_width=True,
        disabled=False
    )
    return edited_df

# Add fragment for the download and history section
@st.fragment
def show_download_and_history(df):
    download_col, history_col = st.columns([1,5])
    with download_col:
        if not df.empty:
            df = h.adjust_column_names_for_download(df)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="members_data.csv",
                mime="text/csv",
                key="download_btn",
                type='primary',
                use_container_width=True
            )
    with history_col:
        with st.expander("View all changes"):
            st.subheader("Edit History")
            if st.session_state.change_log["edited_rows"]:
                st.write("Edited rows:")
                for idx, edits in st.session_state.change_log["edited_rows"].items():
                    for edit in edits:
                        st.write(f"Row {idx} at {edit['timestamp']}:")
                        for col, values in edit['changes'].items():
                            st.write(f"  - {col}: from '{values['from']}' to '{values['to']}'")

# Page Configuration
def setup_page():
    st.set_page_config(
        page_title="AWSCC Data Tool",
        page_icon=":material/analytics:",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Load and apply CSS
    css_path = os.path.join(os.path.dirname(__file__), 'static', 'styles.css')
    with open(css_path) as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

    # Display header image
    st.image(os.path.join(os.path.dirname(__file__), 'static', 'images', 'web-header.svg'))

# Session State Management
def initialize_session_state():
    if "columns_selected" not in st.session_state:
        st.session_state.columns_selected = False
    if "column_selected" not in st.session_state:
        st.session_state.column_selected = False
    if "reset_counter" not in st.session_state:
        st.session_state.reset_counter = 0
    # Add a persistent change log for edits only
    if "change_log" not in st.session_state:
        st.session_state.change_log = {
            "edited_rows": {}
        }

# Filter Controls
def reset_filters():
    st.session_state.reset_counter += 1
    st.session_state.columns_selected = False
    st.session_state.column_selected = False

def render_filter_controls(data):
    reset_key = st.session_state.get('reset_counter', 0)
    
    def on_multiselect_change():
        # Update session state when multiselect changes
        st.session_state.columns_selected = bool(st.session_state[f"multiselect_columns_{reset_key}"])
        if st.session_state.columns_selected:
            st.session_state.column_selected = False

    def on_selectbox_change():
        # Update session state when selectbox changes
        selected_value = st.session_state[f"selectbox_column_{reset_key}"]
        st.session_state.column_selected = bool(selected_value and selected_value != "")
        if st.session_state.column_selected:
            st.session_state.columns_selected = False
    
    # Multi-select for columns
    selected_columns = st.multiselect(
        "Check duplicates & missing values",
        data.columns,
        disabled=st.session_state.column_selected,
        help="Check duplicates or missing values",
        placeholder="Select columns to filter",
        key=f"multiselect_columns_{reset_key}",
        on_change=on_multiselect_change
    )

    # Selectbox for single column
    selected_column = st.selectbox(
        "Inspect a value or similarities",
        [""] + list(data.columns),
        disabled=st.session_state.columns_selected,
        index=0,
        placeholder="Select a column to check",
        help="Search a value or perform string similarity",
        key=f"selectbox_column_{reset_key}",
        on_change=on_selectbox_change
    )

    # Multi-select column options
    duplicates = False
    missing_values = False
    if st.session_state.columns_selected:
        duplicates = st.checkbox("Check for duplicates", key=f"duplicates_{reset_key}")
        missing_values = st.checkbox("Check for missing values", key=f"missing_values_{reset_key}")

    # Single column selection options
    option = None
    search_value = ""
    threshold = 0.8
    if st.session_state.column_selected and not st.session_state.columns_selected:
        option = st.radio("Select option", ["Search", "String similarity"], key=f"option_{reset_key}")
        
        if option == "Search":
            search_value = st.text_input("Search value", key=f"search_value_{reset_key}")
        elif option == "String similarity":
            threshold = st.slider("Threshold", 0.0, 1.0, 0.5, key=f"threshold_{reset_key}")

    # Filter and reset buttons
    col1, col2 = st.columns([1,2])
    with col1:
        st.button("Reset", on_click=reset_filters, type="primary", key=f"reset_{reset_key}", use_container_width=True)
    with col2:
        filter_button = st.button("Apply Filter", type="primary", key=f"filter_{reset_key}", use_container_width=True)

    return selected_columns, selected_column, duplicates, missing_values, option, search_value, threshold, filter_button

# Function to update the change log with edit history
def update_change_log(changes, filtered_df):
    if not changes.get("edited_rows"):
        return
        
    for idx, row_edits in changes.get("edited_rows", {}).items():
        row_num = int(idx)
        if row_num < len(filtered_df):
            orig_idx = filtered_df.index[row_num]
            timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            if str(orig_idx) not in st.session_state.change_log["edited_rows"]:
                st.session_state.change_log["edited_rows"][str(orig_idx)] = []
            
            # Track both old and new values
            changes_with_history = {}
            for col, new_val in row_edits.items():
                old_val = filtered_df.at[orig_idx, col]
                changes_with_history[col] = {
                    "from": old_val,
                    "to": new_val
                }
            
            st.session_state.change_log["edited_rows"][str(orig_idx)].append({
                "timestamp": timestamp,
                "changes": changes_with_history
            })

# Members Tab
def render_members_tab():
    uploaded_data = st.file_uploader(
        "Upload Members Data", 
        type=["csv"], 
        help="Upload a CSV file with members data",
    )

    if uploaded_data is not None:
        # Initialize session state for the dataframe if not already present
        if 'df' not in st.session_state:
            data = pd.read_csv(uploaded_data, index_col=0)
            data = h.clean_column_names(data)
            st.session_state.df = data
            st.session_state.original_df = data.copy()  # Keep original for comparison
        else:
            data = st.session_state.df  # Always use the edited dataframe from session state

        # Use the original dataframe for metrics and visualizations
        original_data = st.session_state.original_df

        # Metric Cards (usingh original_data)
        st.header("Data Quality Check")
        metrics = h.calculate_data_metrics(original_data)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Rows", value=metrics['total_rows'])
        with col2:
            st.metric(label="Unique Webmails", value=metrics['unique_webmails'])
        with col3:
            st.metric(label="Duplicate Webmails", value=metrics['duplicate_webmails'])
        with col4:
            st.metric(label="Non-Webmail Members", value=metrics['non_webmail_members'])

        # Missing Values Chart
        missing_values_fig = viz.create_missing_values_chart(original_data)
        st.plotly_chart(missing_values_fig, use_container_width=True)

        # Text Case Analysis Chart
        text_columns = ['first_name', 'middle_name', 'last_name', 'full_name']
        case_analysis_df = h.analyze_text_case(original_data, text_columns)
        text_case_fig = viz.create_text_case_chart(case_analysis_df)
        st.plotly_chart(text_case_fig, use_container_width=True)

        # Filter and Data Editor Section
        filter_col, data_col = st.columns([1, 4])

        with filter_col:
            st.markdown("#### Filter")
            selected_columns, selected_column, duplicates, missing_values, option, search_value, threshold, filter_button = render_filter_controls(data)
        
        # Apply filters to create a view, but keep the indices to map back to the original dataframe
        filtered_df = data.copy()
        
        # Apply filters when the button is clicked (only affects filtered_df)
        if filter_button:
            if st.session_state.columns_selected and selected_columns:
                conditions = {
                    'duplicates_by_cols': (data.duplicated(subset=selected_columns, keep=False)) & (~data[selected_columns].isna().any(axis=1)), 
                    'missing_values_by_cols': data[selected_columns].isna().any(axis=1)
                }
                
                if duplicates and missing_values:
                    mask = conditions['missing_values_by_cols'] | conditions['duplicates_by_cols']
                elif duplicates:
                    mask = conditions['duplicates_by_cols']
                elif missing_values:
                    mask = conditions['missing_values_by_cols']
                else:
                    mask = pd.Series(True, index=data.index)
                
                filtered_df = data[mask].copy()
            elif st.session_state.column_selected and selected_column:
                if option == "Search" and search_value:
                    filtered_df = data[data[selected_column].str.contains(search_value, na=False)]
                elif option == "String similarity":
                    similar_pairs_df, matching_rows = h.find_similar_strings_with_rows(data, selected_column, threshold)
                    if not matching_rows.empty:
                        filtered_df = matching_rows
                        with st.expander("Similar pairs found"):
                            st.dataframe(similar_pairs_df)

        # Display the data editor with the filtered dataframe
        with data_col:
            st.markdown("#### Interactive Data Inspection")
            editor_key = "data_editor_main"
            
            # Check if we need to save changes from previous edits before showing new filtered data
            if editor_key in st.session_state and 'last_edited_df' in st.session_state:
                changes = st.session_state[editor_key]
                
                if changes.get("edited_rows"):
                    update_change_log(changes, st.session_state.last_edited_df)
                
                if changes.get("edited_rows"):
                    for idx, row_edits in changes.get("edited_rows", {}).items():
                        idx = int(idx)
                        if idx < len(st.session_state.last_edited_df):
                            orig_idx = st.session_state.last_edited_df.index[idx]
                            for col, val in row_edits.items():
                                st.session_state.df.at[orig_idx, col] = val
                    
                    data = st.session_state.df
            
            st.session_state.last_edited_df = filtered_df.copy()
            edited_df = editable_dataframe(filtered_df, editor_key)
            show_download_and_history(st.session_state.df)

# COR Tab
def render_cor_tab():
    st.file_uploader(
        "Upload COR Data", 
        type=["csv"], 
        help="Upload a CSV file with Certificate of Registrations"
    )

# Main Application
def main():
    setup_page()
    initialize_session_state()
    
    members_tab, cor_tab = st.tabs(["Members Data Overview", "Extract COR"])
    
    with members_tab:
        render_members_tab()
    
    with cor_tab:
        render_cor_tab()

if __name__ == "__main__":
    main()