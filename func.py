image_dict = defaultdict(lambda: "https://github.com/faizhalas/Search4All/blob/main/images/perpus.png?raw=true")
image_dict["Buku Ketenaganukliran"] = "https://github.com/faizhalas/Search4All/blob/main/images/bnuklir.png?raw=true"
image_dict["Buku Non-ketenaganukliran"] = "https://github.com/faizhalas/Search4All/blob/main/images/bnonnuklir.png?raw=true"
image_dict["Buku Pedoman"] = "https://github.com/faizhalas/Search4All/blob/main/images/pedoman.png?raw=true"
image_dict["Direktori, annual, yearbook"] = "https://github.com/faizhalas/Search4All/blob/main/images/diranuyear.png?raw=true"
image_dict["Ensiklopedia"] = "https://github.com/faizhalas/Search4All/blob/main/images/ensiklopedia.png?raw=true"
image_dict["Handbook & manual"] = "https://github.com/faizhalas/Search4All/blob/main/images/hanmanu.png?raw=true"
image_dict["Jurnal"] = "https://github.com/faizhalas/Search4All/blob/main/images/jurnal.png?raw=true"
image_dict["Kamus"] = "https://github.com/faizhalas/Search4All/blob/main/images/kamus.png?raw=true"
image_dict["Kerja Praktik"] = "https://github.com/faizhalas/Search4All/blob/main/images/kp.png?raw=true"
image_dict["Prosiding"] = "https://github.com/faizhalas/Search4All/blob/main/images/pros.png?raw=true"
image_dict["Terbitan Internal"] = "https://github.com/faizhalas/Search4All/blob/main/images/ti.png?raw=true"
image_dict["Tugas Akhir"] = "https://github.com/faizhalas/Search4All/blob/main/images/ta.png?raw=true"

def create_card(row, c):
    link = row["url"].strip()
    pict = row["gmd_id"].strip()
    if link != "Sin registro":
        image_link = image_dict[pict]
        clickable_image = f'<a href="{link}" target="_blank"> <img src="{image_link}" style="width:100%;"> </a>'
    else:
        image_link = image_dict["Default"]
        clickable_image = f'<img src="{image_link}" style="width:100%;">'
    with c:
        st.caption(f"{row['gmd_id'].strip()} - {row['year'].strip()}")
        authors_html_list = []
        for author in row["author"].split(";"):
            authors_html_list.append(html_link(author, f"/?author={author}", blank=True))
        authors_html = " | ".join(authors_html_list)
        st.markdown(clickable_image + authors_html, unsafe_allow_html=True)
        st.markdown(f"{row['title'].strip()}")
        
def html_link(text, link, blank=True):
    if blank:
        return f'<a target="_blank" href="{link}">{text}</a>'
    else:
        return f'<a target="_top" href="{link}">{text}</a>'
      
def clickable_image_html(link, image_link, style="width:100%;"):
    html = f'<a href="{link}" target="_blank"><img src="{image_link}" style="{style}"></a>'
    return html
  
def add_style():
    # Define style
    style = """
    a:link {
    color: inherit;
    text-decoration: none;
    }

    a:visited {
    color: inherit;
    text-decoration: none;
    }

    a:hover {
    color: red;
    text-decoration: underline;
    }

    a:active {
    color: red;
    text-decoration: underline;
    }
    """
    my_html = f"""
                <style>
                {style} 
                </style>
                """

    # Execute your app
    st.components.v1.html(my_html, height=0, width=0)

def add_color_to_cards():
    # Define your javascript
    my_js = """
    var cards = window.parent.document.getElementsByClassName("css-vhjbnf");
    for (var i = 0; i < cards.length; i++) {
        let card = cards[i];
        // See if there's content in the card
        N_chars_in_cards = String(card.firstChild.innerHTML).length;
        if (N_chars_in_cards >100){
            card.style.border = "solid";
            card.style.borderColor = "#E4F6F8";
            card.style.borderWidth = "2px";
            card.style.padding = "10px";
            card.style.borderRadius = "10px";
            card.style.borderRadius = "10px";
            card.addEventListener("mouseover", function(event){card.style.borderColor = "red"})
            card.addEventListener("mouseout",  function(event){card.style.borderColor = "#E4F6F8"})
        }
    }    
    """

    # Wrapt the javascript as html code
    my_html = f"""
                <script>
                {my_js}
                </script>
                """
    # Execute your app
    st.components.v1.html(my_html, height=0, width=0)

    return
  
def get_authors_data():
    # Shared gsheet_id
    gsheet_id = "1mdvsYlPVQ0Tda35frF1zoznq9TFtOWe0dKkgWDJkiS0"
    # Data for the authors (authores)
    df_authors = read_googlesheet(gsheet_id, "biblio", ["author"])
    # Add a column with the clean name
    df_authors["author_clean_name"] = df_authors["author"].apply(clean_name)
    # Normalize the column names
    df_authors.columns = [ unidecode(s.lower().strip()) for s in df_authors.columns]
    return df_authors


def is_author_in_authors(df_authors, author):
    """
    """
    author_clean_name = clean_name(author) 
    return author_clean_name in df_authors["author_clean_name"].values


def display_author(df_authors, df_titles, author_search_name):
    """
    """
    # Start the page
    st.caption('Search4All: Author')
    author_clean_name = clean_name(author_search_name)
    # Try to find some talks by the author
    df_author_titles = df_titles.loc[df_titles["author_clean_name"] == author_clean_name, :].reset_index()
    if len(df_author_titles) == 0:
        display_404_author(author_search_name)
        return
    # Get social media for the author
    df_author_links = df_authors.loc[df_authors["author_clean_name"] == author_clean_name, :].reset_index()
    if len(df_author_links) > 0:
        companies_list = ["twitter", "linkedin", "github"]
        known_companies_html = []
        for company in companies_list:
            if company in df_author_links.columns:
                link = df_author_links[company].values[0]
                if len(link)>0:
                    image_link = f"https://github.com/sebastiandres/st_pythonchile/blob/main/images/social_media_icons/{company}.png?raw=true"
                    html = clickable_image_html(link, image_link, style="width:25px;")
                    known_companies_html.append(html)
        html_social_media = "".join(known_companies_html)
    else:
        html_social_media = " "
    # If there is a match, then show the author page
    author_display_name = df_author_titles["author"].values[0]
    st.title(author_display_name)
    st.components.v1.html(html_social_media, height=50)
    # Show the cards
    N_cards_per_col = 5
    for n_row, row in df_author_titles.iterrows():
        i = n_row%N_cards_per_col
        if i==0:
            st.write("")
            cols = st.columns(N_cards_per_col, gap="large")
        create_card(row, cols[n_row%N_cards_per_col])
    add_color_to_cards()
    # Show table!
    #st.write(df_author_links)
    #st.write(df_author_titles)

def display_404_author(author):
    """
    """
    st.title("404")
    st.write(f"No se encontró el author {author} entre los authores registrados.")
    if st.button("Volver a la página principal"):
        st.experimental_set_query_params()  
