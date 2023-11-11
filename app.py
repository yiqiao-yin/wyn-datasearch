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
# Sidebar - Instruction Manual
with st.sidebar:
    with st.expander("Instruction Manual 📖"):
        st.markdown(
            """
            # 🌟 Pyg.Walk Chatbot on Streamlit 🌟

            This Streamlit application serves as a user-friendly interface, similar to Excel or PowerBI dashboards, designed to expedite the navigation and visualization of datasets. Powered by the `pyg.walk` package, it provides a seamless experience, allowing users to traverse their data with speed and efficiency 🚀. The layout is intuitive, presenting data in an organized manner that's easy to analyze at a glance 📊.

            ## 💬 Chatbot Interface

            Behind the scenes, a chatbot interface is integrated into the application, enabling users to interact with their data conversationally 🤖. You can ask the chatbot simple questions regarding your dataset, such as:

            - "What are the column names?" 📝
            - "What is the average of [specific column]?" 📈

            These questions are processed by the chatbot to provide quick, straightforward answers, making data analysis more accessible 🙌.

            ## ⚠️ Limitations

            Please note that the chatbot is designed for basic inquiries only 🛑. It is not equipped to handle complex data analysis or sophisticated queries. To maintain accuracy and avoid potential errors, keep your questions simple. This interface is a prototype aimed at demonstrating the capabilities of `pyg.walk` and should not be used for in-depth analysis 🧐.

            ## 🚀 Getting Started

            To begin, simply drag and drop your dataset in `.csv` format into the designated area of the application 📁➡️📊. Once your file is uploaded, you can start asking your data-related questions in plain English ✍️. The chatbot will respond with the requested information or appropriate guidance on how to phrase your questions for optimal results 💡.

            """
        )
clear_button = st.sidebar.button("Clear Conversation", key="clear")
counter_placeholder = st.sidebar.empty()
st.sidebar.markdown(
    "@ [Yiqiao Yin](https://www.y-yin.io/) | [LinkedIn](https://www.linkedin.com/in/yiqiaoyin/) | [YouTube](https://youtube.com/YiqiaoYin/)"
)



# Initialization
# Session State also supports the attribute based syntax
if 'generated' not in st.session_state:
    st.session_state.generated = []

# Session State also supports the attribute based syntax
if 'past' not in st.session_state:
    st.session_state.past = []

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
            st.session_state["generated"].append(
                {"type": "normal", "data": f"{output}"}
            )

    if st.session_state["generated"]:
        with response_container:
            for i in range(len(st.session_state["generated"])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
                answer = st.session_state["generated"][i]["data"]
                message(answer)
                counter_placeholder.write(f"All rights reserved @ Yiqiao Yin")

else:
    st.warning("Please upload a csv file.")
