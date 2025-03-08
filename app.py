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

