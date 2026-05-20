import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# ----------------------------

llm = ChatMistralAI(model="mistral-small-latest")

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful bug report generator assistant. "
     "You will be given a software issue description and must generate a structured bug report with:\n"
     "1) Summary\n2) Steps to Reproduce\n3) Expected Result\n4) Actual Result."),
    MessagesPlaceholder("history"),
    ("human", "{user_input}")
])
# -------------------------
st.set_page_config(page_title="Bug Report Generator", page_icon="🐞")

st.title("AI Bug Report Generator")
st.write("Turn raw software issues into structured bug reports using AI.")

# session memory
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_area("Describe the software issue:")

if st.button("Generate Bug Report"):

    if not user_input.strip():
        st.warning("Please enter an issue description.")
    else:
        # build prompt with history
        final_prompt = prompt.invoke({
            "history": st.session_state.history,
            "user_input": user_input
        })

        # get response
        result = llm.invoke(final_prompt)

        st.subheader("Generated Bug Report")
        st.write(result.content)

        # save memory
        st.session_state.history.append(HumanMessage(content=user_input))
        st.session_state.history.append(result)


if st.button("Reset History"):
    st.session_state.history = []
    st.success("History cleared!")