import streamlit as st
from streamlit_star_rating import st_star_rating
from PIL import Image
import pandas as pd
import numpy as np
import os

n_movies = 50

# # MovieImage_numbers = os.listdir("MovieImages")
# MovieImage_numbers = [int(n.replace(".jpg", "")) for n in os.listdir("MovieImages")]
#
# movies = pd.read_csv("data/movies.dat",
#                      sep='::', engine = 'python',
#                      encoding="ISO-8859-1", header = None)
# movies.columns = ['MovieID', 'Title', 'Genres']
#
# movies100 = movies[movies["MovieID"].isin(np.random.choice(MovieImage_numbers, n_movies, replace=False))]

movies100 = pd.read_csv("data/movie_subset.csv")

st.set_page_config(layout="wide")

st.title("Movie Recommendations 🎥")
st.write(
    "After rating the movies below, click \"Get Recommendations\" to display movies recommended for you. Scroll to see all movies."
)

user_ratings = dict()

def create_star_rating(Title, MovieID):

    label = Title
    amount_of_stars = 5
    default_value = 0
    size = 15
    emoticons = False
    read_only = False
    dark_theme = False
    reset_btn = True

    customcss = "h3 { font-size: 14px; }"

    def function_to_run_on_click(value):
        user_ratings.update({int(MovieID): value})
        # st.write(f"**{value}** stars!")

    stars = st_star_rating(label, amount_of_stars, default_value, size, emoticons, read_only, dark_theme,
                           resetButton=True, resetLabel="reset",
                               customCSS=customcss, on_click=function_to_run_on_click)


with st.container(height = 500):
    i = 0

    # for col in st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + \
    #            st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + \
    #            st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + \
    #            st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5):

    for col in st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + \
               st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10):
        if i < n_movies:
            with col.container(height=375, border=False):
                m_id = int(movies100["MovieID"].iloc[i])

                img = Image.open("MovieImages/" + str(m_id) + ".jpg")
                img.thumbnail([200, 200], Image.LANCZOS)
                st.write(img)
                movie_title = movies100[movies100["MovieID"] == m_id]["Title"].values[0]
                create_star_rating(movie_title, m_id)

            i += 1

# st.write(user_ratings)

def myIBCF(rated_movies):
    ## for now, return list of movies with any user selected rating
    rated_movies_df = pd.DataFrame.from_dict(rated_movies, orient="index", columns=["rating"])
    return list(rated_movies_df[rated_movies_df["rating"] > 0].index)

def get_recs(rated_movies):
    movie_recs = myIBCF(rated_movies)
    # st.write("movie_recs")
    # st.write(movie_recs)
    # st.write(len(movie_recs))

    if len(movie_recs) == 0:
        st.write("You have not rated any movies")
    else:
        st.write("Recommended for you:")
        show_recs(movie_recs)

def show_recs(rec_ids):
    i = 0
    for col in st.columns(10):
        if i < len(rec_ids):
            with col.container(height = 250, border = False):
                m_id = rec_ids[i]
                img = Image.open("MovieImages/" + str(m_id) + ".jpg")
                img.thumbnail([200, 200], Image.LANCZOS)
                st.write(img)
                movie_title = movies100[movies100["MovieID"] == m_id]["Title"].values[0]
                st.write(movie_title)
            i += 1



if st.button(label = "Get Recommendations!", type = "primary"):
    with st.container():

        # st.write("these are your recommendations:")
        get_recs(user_ratings)
        # st.write(recs_to_show)
        # st.write("user_ratings.keys()")
        # st.write(list(user_ratings.keys()))

