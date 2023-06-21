import streamlit as st
import pdfplumber

def extract_data(feed):
    data = []
    with pdfplumber.open(feed) as pdf:
        pages = pdf.pages
        for p in pages:
            data.append(p.extract_tables())
    return None # build more code to return a dataframe 

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file is not None:
    df = extract_data(uploaded_file)
    st.dataframe(df)
