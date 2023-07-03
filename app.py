import openai
import pandas as pd
import pygwalker as pyg
import streamlit as st
import streamlit.components.v1 as components
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from streamlit_chat import message

# Adjust the width of the Streamlit page
st.set_page_config(page_title="W.Y.N. Data Viz ⭐", layout="wide")

# Add Title
st.title("W.Y.N. Data Viz ⭐")

# Sidebar
clear_button = st.sidebar.button("Clear Conversation", key="clear")
counter_placeholder = st.sidebar.empty()
st.sidebar.markdown(
    "@ [Yiqiao Yin](https://www.y-yin.io/) | [LinkedIn](https://www.linkedin.com/in/yiqiaoyin/) | [YouTube](https://youtube.com/YiqiaoYin/)"
)

# Reset everything
if clear_button:
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state["number_tokens"] = []
    st.session_state["domain_name"] = []
    counter_placeholder.write(f"Next item ...")

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

    # Container for chat history
    response_container = st.container()
    container = st.container()
    with container:
        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_area(
                "Enter your question here:", key="input", height=100
            )
            submit_button = st.form_submit_button(label="Send")

        if submit_button:
            output = pandas_ai(df, prompt=user_input)
            st.session_state["past"].append(user_input)
            st.session_state["generated"].append({"type": "normal", "data": f"{output}"})

    if st.session_state["generated"]:
        with response_container:
            for i in range(len(st.session_state["generated"])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
                answer = st.session_state["generated"][i]["data"]
                message(answer)
                counter_placeholder.write(f"All rights reserved @ Yiqiao Yin")

else:
    st.warning("Please upload a csv file.")
