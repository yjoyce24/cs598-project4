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
    size = 20
    emoticons = False
    read_only = False
    dark_theme = False
    reset_btn = True

    customcss = "h3 { font-size = 12px; color:red; } "

    def function_to_run_on_click(value):
        user_ratings.update({MovieID: value})
        # st.write(f"**{value}** stars!")

    stars = st_star_rating(label, amount_of_stars, default_value, size, emoticons, read_only, dark_theme,
                           resetButton=False, resetLabel="",
                               customCSS=customcss, on_click=function_to_run_on_click)
    st.write(stars)


i = 1


# allrows = exec(" + ".join(np.repeat("st.columns(5)", 20)))


for col in st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10) + st.columns(10):

    if i <= 100:
        with col.container(height = 450):
            img = Image.open("MovieImages/" + str(i) + ".jpg")
            img.thumbnail([200, 200], Image.LANCZOS)
            st.write(img)
            movie_title = movies[movies["MovieID"] == i]["Title"].values[0]
            create_star_rating(movie_title, i)

        i += 1


#
# row1 = st.columns(10)
# row2 = st.columns(10)
# row3 = st.columns(10)
# row4 = st.columns(10)
# row5 = st.columns(10)
# row6 = st.columns(10)
# row7 = st.columns(10)
# row8 = st.columns(10)
# row9 = st.columns(10)
# row10 = st.columns(10)
#
# i = 1
# for col in row1 + row2 + row3 + row4 + row5 + row6 + row7 + row8 + row9 + row10:
#     with st.container(height=120):
#         img = Image.open("MovieImages/" + str(i) + ".jpg")
#         st.write(img)
#         movie_title = movies[movies["MovieID"] == i]["Title"].values[0]
#         create_star_rating(movie_title, i)
#         i += 1


st.write(user_ratings)

