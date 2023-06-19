# Import libraries
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Python Talks Search Engine", page_icon="🐍", layout="wide")
st.title("Python Talks Search Engine")

# Connect to the Google Sheet
sheet_id = "1mdvsYlPVQ0Tda35frF1zoznq9TFtOWe0dKkgWDJkiS0"
sheet_name = "bibliograph"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str, header=0)
#df = df.sort_values('biblio_id', ascending=False, ignore_index=True)

# Show the dataframe (we'll delete this later)
st.write(df)

# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("Search videos by title or speaker", value="")

st.title('Search4All: Recorded materials')
# Intro text
st.caption(f"Discover and learn among the more than **{df.shape[0]}** sources available from Search4All.")
c1, c2, c3 = st.columns([6,1,3])
# The search bar
exampless = ["data science", "machine learning", "nuclear", "mechanic"]
if "examples" not in st.session_state:
 st.session_state.examples = exampless[random.randint(0, len(exampless)-1)]
text_search = c1.text_input("Search by author, title, or full-text. Separate concepts by semicolons (;)",
              placeholder=st.session_state.examples)
text_search = unidecode(text_search.lower())
# Get keywords from search bar
keyword_list = [keyword.strip() for keyword in text_search.split(";")]
st.write(keyword_list)
# Add options
talk_options = ["All", "Buku Ketenaganukliran", "Buku Non-ketenaganukliran", "Buku Pedoman", "Direktori, annual, yearbook", "Ensiklopedia", "Handbook & manual", "Jurnal", "Kamus", "Kerja Praktik", "Prosiding", "Terbitan Internal", "Tugas Akhir"]
type_sel = c2.selectbox("Type", talk_options)
#c3.markdown(""); c3.markdown(""); 
search_opt = c3.multiselect(
        "Search fields",
        ["author", "title", "full-text"],
        ["author", "title"])
