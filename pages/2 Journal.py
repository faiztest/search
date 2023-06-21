import streamlit as st
#===config===
st.set_page_config(
     page_title="Pencarian Terpadu",
     page_icon="https://digilib.polteknuklir.ac.id/perpus/images/default/logo.png",
     layout="wide"
)
st.write('hello')
uploaded_files = st.file_uploader("Choose your a file", type=['pdf'], on_change=reset_data, accept_multiple_files=True)
