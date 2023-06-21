import streamlit as st
import pdfplumber
import pandas as pd

def cache_clear():
    st.cache_data.clear()

@st.cache_data(experimental_allow_widgets=True)
def convert(uploaded_files):
    data = []
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        data.append({"File Name": file.name, "Text": text})
    return data

st.title("PDF to Text Converter")
st.header("Upload PDF Files")

uploaded_files = st.file_uploader("Choose files", type=['pdf'], accept_multiple_files=True, on_change=cache_clear)

if uploaded_files is not None:
    st.subheader("Extracted Text")
    extracted_data = convert(uploaded_files)
    df = pd.DataFrame(extracted_data)
    st.dataframe(df)
