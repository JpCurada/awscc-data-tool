import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AWSCC Data Tool",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open(r"static\styles.css") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


st.title("Dashboard Tool")

