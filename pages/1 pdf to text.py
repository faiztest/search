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
    data = []
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        data.append({"File Name": file.name, "Text": text})
    df = pd.DataFrame(data).replace(r'\n',' ', regex=True)
    return df

@st.cache_data(ttl=3600, experimental_allow_widgets=True)
def convert_col(uploaded_files):
    x0 = 0    # Distance of left side of character from left side of page.
    #x1 = 0.5  # Distance of right side of character from left side of page.
    y0 = 0  # Distance of bottom of character from bottom of page.
    y1 = 1  # Distance of top of character from bottom of page.
 
    data = []
    for file in uploaded_files:
        all_content = [] 
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

@st.cache_data(ttl=3600)
def remove_sen(df):
    for sentence in remove_list:
         df['Text'] = df['Text'].str.replace(sentence, '')


st.title("PDF to Text Converter")
st.header("Upload PDF Files")

uploaded_files = st.file_uploader("Choose files", type=['pdf'], accept_multiple_files=True)

col1, col2 = st.columns(2)
with col1:
     rmv = st.text_input("Remove certain text before 'your text'.")
with col2:
     rmv_text = st.text_input("Remove certain text on your PDF. Separate by semicolons (;).")
     remove_list = [keyword.strip() for keyword in rmv_text.split(";")]


text_search = st.text_input("Split your PDFs into parts. Separate words (cAsE sEnSiTiVe) by semicolons (;)", "INTRODUCTION")
word_list = [keyword.strip() for keyword in text_search.split(";")]

have_column = st.checkbox('PDF has 2 columns')
if have_column:
     x1 = st.number_input('Distance of right side of character from left side of page.', min_value=0.0, max_value=1.0, value=0.5)

if st.button("Convert", on_click=clear_data):
    try:
         if have_column:
              df = convert_col(uploaded_files)
         else:
              df = convert(uploaded_files)
         rdf = remove_before(df)
         rdf = remove_sen(rdf)
         result_df = split(rdf)
    except ValueError:
            st.error('Error: Please double-check the words that are used as splitter.')
            sys.exit(1)
         
    if not result_df.empty:
        st.subheader("Extracted Text")
        st.dataframe(result_df)
