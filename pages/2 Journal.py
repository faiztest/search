import streamlit as st
#===config===
st.set_page_config(
     page_title="Pencarian Terpadu",
     page_icon="https://digilib.polteknuklir.ac.id/perpus/images/default/logo.png",
     layout="wide"
)
st.write('hello there')
uploaded_files = st.file_uploader("Choose your a file", type=['pdf'], accept_multiple_files=True)
uploaded_file = st.file_uploader("Choose a file")
