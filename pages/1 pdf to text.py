import streamlit as st
import PyPDF2
import pandas as pd
import os

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
    if uploaded_files:
        data = []
        for file in uploaded_files:
            file_name = file.name
            file_path = os.path.join("uploads", file_name)  # Save file locally
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            text = convert_pdf_to_text(file_path)
            data.append({"File Name": file_name, "Text": text})
            os.remove(file_path)  # Remove the file after processing

        df = pd.DataFrame(data)
        st.subheader("Extracted Text")
        st.dataframe(df)

st.title("PDF to Text Converter")
st.header("Upload PDF Files")

uploaded_files = st.file_uploader("Choose your file", type=['pdf'], on_change=reset_data, accept_multiple_files=True)

if uploaded_files:
    main()
