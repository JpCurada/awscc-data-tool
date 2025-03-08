import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="AWSCC Data Tool",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

css_path = os.path.join(os.path.dirname(__file__), 'static', 'styles.css')
with open(css_path) as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


st.title("Dashboard Tool")

uploaded_data =st.file_uploader("Upload a file", type=["csv"], help="Upload a CSV file for processing")
st.markdown('---')

if uploaded_data:
    df = pd.read_csv(uploaded_data)
    
    
    dashboard_tab, quality_check_tab, cleaning_tab = st.tabs(["Dashboard", "Quality Check", "Cleaning"])
    
    with quality_check_tab:

        st.header("Summary Report")

        # Missing Values
        st.markdown(f"""
        # Missinng Values
        {df.isnull().sum()}
        # Missing Values Percentage
        {df.isnull().mean()}
        # Duplicates
        There are {df.duplicated().sum()} duplicate rows in the dataset
        There are {df.duplicated('pup_webmail').sum()} duplicate rows based on PUP Webmail.
                    
                    """)

        # Duplicates

        # Data Types

        # Name Inconsistencies

        st.markdown('---')

        st.header("Data Quality Checker")
        st.caption("Use filters to inspect the quality of the data")
        
        filter_col, display_col = st.columns([1,3])
        
        display_col.data_editor(df)

        filter_col.multiselect("Inspect Columns", options=df.columns, placeholder="Select Columns (Default All Columns)")
        filter_col.multiselect(label="Check for duplicates", options=df.columns, placeholder="Select Columns")
        filter_col.multiselect("Check for missing values", options=df.columns, placeholder="Select Columns")
