import streamlit as st
import pandas as pd
from utils import (
    clean_column_names,
    standardize_birthday_col,
    standardize_text_data,
    detect_duplicates_by_cols,
    detect_missing_val_by_cols
)
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


st.image(os.path.join(os.path.dirname(__file__), 'static', 'images', 'web-header.svg'))

uploaded_data =st.file_uploader("Upload a file", type=["csv"], help="Upload a CSV file for processing")
st.markdown('---')

if uploaded_data:
    df = pd.read_csv(uploaded_data)
    df = clean_column_names(df)
    dashboard_tab, quality_check_tab, cleaning_tab = st.tabs(["Dashboard", "Quality Check", "Cleaning"])
    
    with quality_check_tab:

        st.header("Summary Report")

        # Missing Values
        st.markdown(f"""
        There are {df['pup_webmail'].nunique()} members based on unique PUP Webmails in the dataset. 
        
        There are  {len(detect_duplicates_by_cols(df, ['pup_webmail']))} duplicates based on PUP Webmail. 

                    """)

        # Duplicates
        # Check if there are duplicate rows
        # Check if there are duplicate rows based on webmail
        # Check if there are duplicate rows based on first_name and last_name


        # Data Types
        # Check if there are columns that are in the wrong data types(must be datetime, int, float, or categorical)

        # Name Inconsistencies
        # Check if there are first_name and last_name that has same values
        # Count of row that is in uppercase, title_case, and lowercase for full name
        # Check if there are names that has special characters
        # Ch

        st.markdown('---')

        st.header("Data Quality Checker")
        st.caption("Use filters to inspect the quality of the data")
        
        filter_col, display_col = st.columns([1,3])
        
        display_col.data_editor(df)


        filter_col.multiselect(label="Check for duplicates", options=df.columns, placeholder="Select Columns")
        filter_col.multiselect("Check for missing values", options=df.columns, placeholder="Select Columns")
        filter_col.multiselect("Check for similar names", options=df.columns, placeholder="Select Columns")
