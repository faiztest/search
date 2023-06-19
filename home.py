# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import re
from unidecode import unidecode

# Page setup
st.set_page_config(page_title="Python Talks Search Engine", page_icon="🐍", layout="wide")
st.title("Python Talks Search Engine")

# Connect to the Google Sheet
sheet_id = "1mdvsYlPVQ0Tda35frF1zoznq9TFtOWe0dKkgWDJkiS0"
sheet_name = "bibliograph"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str, header=0)
df = df.sort_index(ascending=False)

st.title('Search4All: Recorded materials')
# Intro text
st.caption(f"Discover and learn among the more than **{df.shape[0]}** sources available from Search4All.")
c1, c2, c3 = st.columns([6,1,3])
# The search bar
text_search = c1.text_input("Search by author, title, or full-text. Separate concepts by semicolons (;)")
#text_search = unidecode(text_search.lower())
# Get keywords from search bar
keyword_list = [keyword.strip() for keyword in text_search.split(";")]
st.write(keyword_list)
# Add options
format_options = ["All", "Buku Ketenaganukliran", "Buku Non-ketenaganukliran", "Buku Pedoman", "Direktori, annual, yearbook", "Ensiklopedia", "Handbook & manual", "Jurnal", "Kamus", "Kerja Praktik", "Prosiding", "Terbitan Internal", "Tugas Akhir"]
type_for = c2.selectbox("Type", format_options)
search_opt = c3.multiselect(
        "Search fields",
        ["author", "title", "full-text"],
        ["author", "title"])

if keyword_list is not None:        
        key_df = pd.DataFrame(columns=['biblio_id', 'url', 'gmd_id', 'title', 'author', 'year', 'callnum', 'full-text'])
        patterns = [r'\b{}\b'.format(re.escape(word)) for word in keyword_list]

        for col in columns:
            conditions = [df[col].str.contains(pattern, regex=True, flags=re.IGNORECASE) for pattern in patterns]
            column_result = df[np.logical_and.reduce(conditions)]
            key_df = pd.concat([key_df, column_result])

        st.write(key_df)
        
if type_for != format_options[0]:
        res_df = key_df[key_df['gmd_id'].str.contains(type_for)]
        st.write(res_df)
        
        
        
#for col in search_opt:
#        mat = res_df[col].apply(lambda x: any(w in x for w in keyword_list))
#        listmat.append(mat)



# Show the dataframe (we'll delete this later)
#st.write(listmat)
