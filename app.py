import openai
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import pygwalker as pyg
import streamlit as st
import streamlit.components.v1 as components

# Adjust the width of the Streamlit page
st.set_page_config(page_title="W.Y.N. Data Viz ⭐", layout="wide")

# Add Title
st.title("W.Y.N. Data Viz ⭐")

# Insert a file uploader that accepts multiple files at a time
uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file is not None:
    # Success message
    st.success("File uploaded successfully.")

    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)

    # Generate the HTML using Pygwalker
    pyg_html = pyg.walk(df, return_html=True)

    # Embed the HTML into the Streamlit app
    components.html(pyg_html, height=1000, scrolling=True)

    # Instantiate a LLM
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    llm = OpenAI(api_token=OPENAI_API_KEY)
    pandas_ai = PandasAI(llm)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # React to user input
    if prompt := st.chat_input("Enter key words here."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Get answer
    response = pandas_ai(df, prompt=prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear
    counter_placeholder = st.sidebar.empty()
    clear_button = st.button("Clear Conversation", key="clear")

    # reset everything
    if clear_button:
        st.session_state["generated"] = []
        st.session_state["past"] = []
        st.session_state["messages"] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        st.session_state["number_tokens"] = []
        st.session_state["domain_name"] = []
        counter_placeholder.write(f"Next item ...")
else:
    st.warning("Please upload a csv file.")
