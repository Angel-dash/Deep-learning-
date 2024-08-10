import sys
import streamlit as st
import os
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from commons.settings import model

##function to load gemini pro vision

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

st.set_page_config(page_title= "Multilanguage invoice extractor")
st.header("Gemini Application")
input = st.text_input("Input Prompt: ", key= "input")
uploaded_file = st.file_uploader("Choose an image of the invoice:", type = ["jpeg","jpg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption ="Uploaded Image",use_column_width=True)

submit = st.button("Tell me about the invoice")