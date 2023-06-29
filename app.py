import pandas as pd
import pygwalker as pyg
import streamlit as st
import streamlit.components.v1 as components

# Adjust the width of the Streamlit page
st.set_page_config(page_title="W.Y.N. Data Search", layout="wide")


# Add Title
st.title("Use Pygwalker In Streamlit")


# Upload csv
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)


# Import your data
# Can be used wherever a "file-like" object is accepted:
try:
    df = pd.read_csv(uploaded_file)
except:
    df = pd.read_csv(
        "https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv"
    )


# Generate the HTML using Pygwalker
pyg_html = pyg.walk(df, return_html=True)


# Embed the HTML into the Streamlit app
components.html(pyg_html, height=1000, scrolling=True)
