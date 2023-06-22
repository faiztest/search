import streamlit as st
import pdfplumber
import pandas as pd
import streamlit.components.v1 as components

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

uploaded_files = st.file_uploader("Choose files", type=['pdf'], accept_multiple_files=True)
text_search = st.text_input("Split your PDFs into parts. Separate words (cAsE sEnSiTiVe) by semicolons (;)")
word_list = [keyword.strip() for keyword in text_search.split(";")]
st.write(word_list)

if st.button("Convert"):
    extracted_data = convert(uploaded_files)
    df = pd.DataFrame(extracted_data)
    df = df.replace(r'\n',' ', regex=True) 
    if not df.empty:
        st.subheader("Extracted Text")
        st.data_editor(df)
