# Import libraries
import streamlit as st
import pandas as pd
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
text_search = unidecode(text_search.lower())
# Get keywords from search bar
keyword_list = [keyword.strip() for keyword in text_search.split(";")]
# Add options
format_options = ["All", "Buku Ketenaganukliran", "Buku Non-ketenaganukliran", "Buku Pedoman", "Direktori, annual, yearbook", "Ensiklopedia", "Handbook & manual", "Jurnal", "Kamus", "Kerja Praktik", "Prosiding", "Terbitan Internal", "Tugas Akhir"]
type_for = c2.selectbox("Type", format_options)
#c3.markdown(""); c3.markdown(""); 
search_opt = c3.multiselect(
        "Search fields",
        ["author", "title", "full-text"],
        ["author", "title"])

if type_sel != talk_options[0]:
        res_df = df.loc[df['gmd_id'].isin(format_options)]
       
st.write(res_df)

listmat = None
for col in search_opt:
        mat = res_df[col].apply(lambda x: any(w in x for w in keyword_list))
        listmat.append(mat)



# Show the dataframe (we'll delete this later)
st.write(listmat)
