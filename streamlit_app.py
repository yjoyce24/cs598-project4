import streamlit as st
from streamlit_star_rating import st_star_rating
from PIL import Image
import pandas as pd
import numpy as np
import os

n_movies = 10

# MovieImage_numbers = os.listdir("MovieImages")
MovieImage_numbers = [int(n.replace(".jpg", "")) for n in os.listdir("MovieImages")]

movies = pd.read_csv("data/movies.dat",
                     sep='::', engine = 'python',
                     encoding="ISO-8859-1", header = None)
movies.columns = ['MovieID', 'Title', 'Genres']

movies100 = movies[movies["MovieID"].isin(np.random.choice(MovieImage_numbers, n_movies, replace=False))]

st.set_page_config(layout="wide")

st.title("Movie Recommendations 🎥")
st.write(
    "Rate each movie below to get a list of movie recommendations."
)

user_ratings = dict()

def create_star_rating(Title, MovieID):

    label = Title
    amount_of_stars = 5
    default_value = 0
    size = 20
    emoticons = False
    read_only = False
    dark_theme = False
    reset_btn = True

    customcss = "h3 { font-size: 16px; }"

    def function_to_run_on_click(value):
        user_ratings.update({MovieID: value})
        # st.write(f"**{value}** stars!")

    stars = st_star_rating(label, amount_of_stars, default_value, size, emoticons, read_only, dark_theme,
                           resetButton=False, resetLabel="",
                               customCSS=customcss, on_click=function_to_run_on_click)
    st.write(stars)


i = 0

for col in st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10):
    if i < n_movies:
        with col.container(height=400):
            m_id = int(movies100["MovieID"].iloc[i])

            img = Image.open("MovieImages/" + str(m_id) + ".jpg")
            img.thumbnail([200, 200], Image.LANCZOS)
            st.write(img)
            movie_title = movies[movies["MovieID"] == m_id]["Title"].values[0]
            create_star_rating(movie_title, m_id)

        i += 1

st.write(user_ratings)

def myIBCF(rated_movies):
    ## for now, output ids of 10 movies
    return np.random.choice(list(rated_movies.keys()), 10, replace=False)

def get_recs():
    movie_recs = myIBCF(user_ratings)

# st.button("fake button")

if st.button(label = "Get Recommendations!"):
    with st.container():
        recs_to_show = get_recs()
        st.write(recs_to_show)
        st.write("these are your recommendations")
