import json
import sys
import streamlit as st
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from commons.settings import model


def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text


##Initialize our streamlit app

st.set_page_config(page_title="Q&A Demo", layout="wide")

st.header("Gemini LLM Application")

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

##When submit is click

if submit:
    response = get_gemini_response(input)
    st.subheader("The response is:")
    st.write(response)
