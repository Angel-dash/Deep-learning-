import sys
import streamlit as st
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from commons.settings import model
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

#initiliaze session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    ##Add user query and response to session chat history.
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The response is ")
    for chunk in response:
        # st.write(chunk)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("The chat history is ")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
