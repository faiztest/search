import streamlit as st
import pdfplumber

def cache_clear():
    st.cache_data.clear()

@st.cache_data(experimental_allow_widgets=True)
def convert(uploaded_files):
    results = []
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        results.append(text)
    return results

st.title("PDF to Text Converter")
st.header("Upload PDF Files")

uploaded_files = st.file_uploader("Choose files", type=['pdf'], accept_multiple_files=True, on_change=cache_clear)

if uploaded_files is not None:
    st.subheader("Extracted Text")
    extracted_texts = convert(uploaded_files)
    for i, text in enumerate(extracted_texts):
        file_name = uploaded_files[i].name
        st.subheader(file_name)
        st.text_area(f"Text {i+1}", value=text, height=400)
