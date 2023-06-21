import streamlit as st
import PyPDF2
import pandas as pd

# === config ===
st.set_page_config(
    page_title="Pencarian Terpadu",
    page_icon="https://digilib.polteknuklir.ac.id/perpus/images/default/logo.png",
    layout="wide"
)

def reset_data():
    st.cache_data.clear()

def convert_pdf_to_text(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        num_pages = reader.numPages
        for page_num in range(num_pages):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text

def main():
    if uploaded_file is not None:
        file_name = uploaded_file.name
        text = convert_pdf_to_text(uploaded_file)
        data = [{"File Name": file_name, "Text": text}]
        df = pd.DataFrame(data)
        st.subheader("Extracted Text")
        st.dataframe(df)

st.title("PDF to Text Converter")
st.header("Upload PDF File")

uploaded_file = st.file_uploader("Choose a file", type=['pdf'], on_change=reset_data)

if uploaded_file is not None:
    main()
