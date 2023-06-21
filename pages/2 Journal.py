import streamlit as st
import pdfplumber

def cache_clear():
    st.cache_data.clear()

@st.cache_data
def main(uploaded_file):

    if uploaded_file is not None:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        st.text_area("Text", value=text, height=400)


st.title("PDF to Text Converter")
st.header("Upload PDF File")
uploaded_file = st.file_uploader("Choose a file", type=['pdf'], on_change=cache_clear)

if uploaded_file is not None:
    st.subheader("Extracted Text")
    main(uploaded_file)
