import json
import sys
import streamlit as st
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image
from commons.settings import genai
model = genai.GenerativeModel("models/gemini-1.5-flash")


def get_gemini_response(input, image):
    if input != "":
        response = model.generate_content([input, image])
        return response.text
    else:
        response = model.generate_content(image)
    return response.text


##Initialize our streamlit app

st.set_page_config(page_title="Gemini-Image-demo", layout="wide")

st.header("Gemini LLM Application")

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

uploaded_file = st.file_uploader("Choose an image...", type=["jpeg", "jpg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)



submit = st.button("Tell me about the image")
if submit:
    response = get_gemini_response(input, image)
    st.subheader("The response is :")
    st.write(response)
