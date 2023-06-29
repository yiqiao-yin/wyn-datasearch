import pandas as pd
import pygwalker as pyg
import streamlit as st
import streamlit.components.v1 as components

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)
 
# Add Title
st.title("Use Pygwalker In Streamlit")

# Insert a file uploader that accepts multiple files at a time
uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)

    # Generate the HTML using Pygwalker
    pyg_html = pyg.walk(df, return_html=True)

    # Embed the HTML into the Streamlit app
    components.html(pyg_html, height=1000, scrolling=True)