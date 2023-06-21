import streamlit as st
import pdfplumber

def main(uploaded_file):
    st.title("PDF to Text Converter")

    if uploaded_file is not None:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        st.subheader("Extracted Text")
        st.text_area("Text", value=text, height=400)

def reset_data():
    st.cache_data.clear()

st.header("Upload PDF File")
uploaded_file = st.file_uploader("Choose a file", type=['pdf'], on_change=reset_data)

if uploaded_file is not None:
    main(uploaded_file)
