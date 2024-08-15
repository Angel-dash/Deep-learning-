import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings

import google.generativeai as genai
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_pdf_text(pdf_docs):
    """
    This function reads pdf documents and extracts text from it.
    :param pdf_docs:
    :return:
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    """
    This function is used to divide the text into different chunks
    :param text:
    :return:
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    """
    Vector embeddings of each of the chunks and storing it locally
    :param text_chunks:
    :return:
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. Make sure to provide all the details. If the answer is not in 
    the provided context, just say, "Answer is not available in the context". Don't provide a wrong answer.

    Context: {context}

    Question: {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # Use LLMChain instead of load_qa_chain
    chain = LLMChain(llm=model, prompt=prompt)
    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    # Prepare the context by joining the page_content of all documents
    context = "\n".join([doc.page_content for doc in docs])

    # Use the chain with the correct input format
    response = chain.invoke({
        "context": context,
        "question": user_question
    })

    print(response)
    st.write("Reply:", response["text"])  # Changed from "output_text" to "text"


def main():
    st.set_page_config("Chat with multiple PDF")
    st.header("Chat with multiple PDF using Gemini💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button",
                                    accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")


if __name__ == "__main__":
    main()
