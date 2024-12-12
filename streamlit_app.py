import streamlit as st
from streamlit_star_rating import st_star_rating
from PIL import Image
import pandas as pd
import numpy as np

movies = pd.read_csv("data/movies.dat",
                     sep='::', engine = 'python',
                     encoding="ISO-8859-1", header = None)
movies.columns = ['MovieID', 'Title', 'Genres']

movies100 = movies.iloc[np.random.choice(range(movies.shape[0]), 100, replace=False)]

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
    size = 40
    emoticons = False
    read_only = False
    dark_theme = False
    reset_btn = True

    def function_to_run_on_click(value):
        user_ratings.update({MovieID: value})
        # st.write(f"**{value}** stars!")

    stars = st_star_rating(label, amount_of_stars, default_value, size, emoticons, read_only, dark_theme,
                           resetButton=False, resetLabel="",
                               customCSS="", on_click=function_to_run_on_click)
    st.write(stars)

for i in range(1,6):
    img = Image.open("MovieImages/" + str(i) + ".jpg")
    st.write(img)
    movie_title = movies[movies["MovieID"] == i]["Title"].values[0]
    st.write(movie_title)
    create_star_rating(movie_title, i)


st.write(user_ratings)

