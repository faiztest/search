import streamlit as st
import pdfplumber
import pandas as pd
import streamlit.components.v1 as components
import sys

st.set_page_config(
     page_title="PDFs to dataframe",
     page_icon="https://github.com/faizhalas/Search4All/blob/main/images/logo.png?raw=true",
     layout="wide"
)

def clear_data():
     st.cache_data.clear()

@st.cache_data(ttl=3600, experimental_allow_widgets=True)
def convert(uploaded_files):
    x0 = 0    # Distance of left side of character from left side of page.
    x1 = 0.5  # Distance of right side of character from left side of page.
    y0 = 0  # Distance of bottom of character from bottom of page.
    y1 = 1  # Distance of top of character from bottom of page.
 
    data = []
    all_content = [] 
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            for i, page in enumerate(pdf.pages):
                 width = page.width
                 height = page.height
          
                 # Crop pages
                 left_bbox = (x0*float(width), y0*float(height), x1*float(width), y1*float(height))
                 page_crop = page.crop(bbox=left_bbox)
                 left_text = page_crop.extract_text()
          
                 left_bbox = (0.5*float(width), y0*float(height), 1*float(width), y1*float(height))
                 page_crop = page.crop(bbox=left_bbox)
                 right_text = page_crop.extract_text()
                 page_context = '\n'.join([left_text, right_text])
                 all_content.append(page_context)
                 text = '\n'.join(all_content)
                 
        data.append({"File Name": file.name, "Text": text})
    df = pd.DataFrame(data).replace(r'\n',' ', regex=True)
    return df

@st.cache_data(ttl=3600)
def remove_before(df):
    if rmv:
         df['Text'] = df['Text'].str.split(rmv).str[-1].str.strip()
    return df


@st.cache_data(ttl=3600)
def split(extracted_data):
    pattern = '|'.join(word_list)
    split_df = df['Text'].str.split(pattern, expand=True)
    result_df = pd.concat([df, split_df], axis=1)
    new_columns = ['File Name', 'Text', 'intro'] + word_list
    result_df.columns = new_columns
    return result_df    


st.title("PDF to Text Converter")
st.header("Upload PDF Files")

uploaded_files = st.file_uploader("Choose files", type=['pdf'], accept_multiple_files=True)

rmv = st.text_input("Remove certain text before 'your text'.")

text_search = st.text_input("Split your PDFs into parts. Separate words (cAsE sEnSiTiVe) by semicolons (;)")
word_list = [keyword.strip() for keyword in text_search.split(";")]

if st.button("Convert", on_click=clear_data):
         df = convert(uploaded_files)
         st.write(df)
         rdf = remove_before(df)
         st.write(rdf)
         result_df = split(rdf)
         st.write(result_df)
         st.subheader("Extracted Text")
         st.dataframe(result_df)
