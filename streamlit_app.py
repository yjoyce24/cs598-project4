import streamlit as st
from streamlit_star_rating import st_star_rating
from PIL import Image
import pandas as pd
import numpy as np
import os

n_movies = 100

# read in subset of movies.dat (top 100 most popular movies out of those with images)
movies100 = pd.read_csv("data/movies100.csv")

# read in Rmat for the movies in movies100
Rmat100 = pd.read_csv("data/Rmat100.csv", index_col=0)
Rmat100_cols = Rmat100.columns

# read in top 30 similarity matrix for movies in movies100
Smat = pd.read_csv("data/top_30_S_matrix.csv").to_numpy()

st.set_page_config(layout="wide")

st.title("Movie Recommendations 🎥")
st.write(
    "After rating the movies below, click \"Get Recommendations\" to display movies recommended for you. Scroll to see all movies."
)

user_ratings_dict = dict()

movie_ids = list(Rmat100.columns)

def mostpopular(R_mat,n):
  total_ratings = np.nansum(R_mat,axis=0)
  top_n_indices = np.argsort(total_ratings)[::-1][:n]
  top_n_movies = [movie_ids[i] for i in top_n_indices]
  return top_n_movies,top_n_indices

def create_star_rating(Title, MovieID):
    label = Title
    amount_of_stars = 5
    default_value = 0
    size = 20
    emoticons = False
    read_only = False
    dark_theme = False
    reset_btn = True

    customcss = "h3 { font-size: 14px; } " \
                "[data-baseweb=\"button\"] {padding: 2px 5px; border-radius: 5px; font-size: 10px;}"

    def function_to_run_on_click(value):
        user_ratings_dict.update({int(MovieID): value})
        # st.write(f"**{value}** stars!")

    stars = st_star_rating(label, amount_of_stars, default_value, size, emoticons, read_only, dark_theme,
                           resetButton=True, resetLabel="reset",
                               customCSS=customcss, on_click=function_to_run_on_click)


rate_movies_exp = st.expander(rf"""**Add Movie Ratings**""", expanded=True)

with rate_movies_exp.container(height = 450):
    m = 0

    for col in st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + \
               st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + \
               st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + \
               st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5) + st.columns(5):
        if m < n_movies:
            with col.container(height=375, border=False):
                m_id = int(movies100["MovieID"].iloc[m])

                img = Image.open("MovieImages/" + str(m_id) + ".jpg")
                img.thumbnail([200, 200], Image.LANCZOS)
                st.write(img)
                movie_title = movies100[movies100["MovieID"] == m_id]["Title"].values[0]
                create_star_rating(movie_title, m_id)

            m += 1

# st.write(user_ratings_dict)


def myIBCF(new_user_ratings, similarity_matrix):
  predicted_ratings = np.full_like(new_user_ratings,np.nan,dtype=float)
  for i in range(similarity_matrix.shape[0]):
    similarity = similarity_matrix[i, :]
    common_mask = ~np.isnan(new_user_ratings) & ~np.isnan(similarity)
    similarity = similarity[common_mask]
    ratings = new_user_ratings[common_mask]
    num = np.dot(similarity,ratings)
    den = np.sum(similarity)
    if den == 0:
      predicted_ratings[i] = np.nan
    else:
      predicted_ratings[i] = num/den
  non_nan_mask = ~np.isnan(new_user_ratings)
  predicted_ratings[non_nan_mask] = np.nan
  not_nan = ~np.isnan(predicted_ratings)
  predicted_ratings1 = predicted_ratings[not_nan]

  st.write(predicted_ratings1)

  if len(predicted_ratings1) < 10:
    m,id = mostpopular(Rmat100,10-len(predicted_ratings1))
    top_n_indices_in_sorted_non_nan = np.argsort(predicted_ratings1)[::-1][:10]
    top_n_movie_ID = np.where(not_nan)[0][top_n_indices_in_sorted_non_nan]
    top_10_movie_ID = np.concatenate((top_n_movie_ID,id))
    top_10_movies = [movie_ids[i] for i in top_10_movie_ID]
    top_10_values = np.array(predicted_ratings1[top_n_indices_in_sorted_non_nan].tolist() + [0] * (10 - len(predicted_ratings1)))
  else:
    top_10_indices_in_sorted_non_nan = np.argsort(predicted_ratings1)[::-1][:10]
    top_10_movie_ID = np.where(not_nan)[0][top_10_indices_in_sorted_non_nan]
    top_10_movies = [movie_ids[i] for i in top_10_movie_ID]
    top_10_values = predicted_ratings1[top_10_indices_in_sorted_non_nan]

  return top_10_movies, top_10_values

def get_recs(rated_movies):
    rated_movies_df = pd.DataFrame.from_dict(rated_movies, orient="index", columns=["rating"])
    rated_movies_list = list(rated_movies_df[rated_movies_df["rating"] > 0].index)

    if len(rated_movies_list) == 0:
        st.write("You have not rated any movies")
    else:
        ratings = np.full(len(Rmat100_cols), np.nan)

        for k in rated_movies.keys():
            idx = np.where(np.isin(Rmat100_cols, "m" + str(k)))[0]
            # st.write(idx)
            ratings[idx] = rated_movies.get(k)

        # st.write(ratings)
        movie_recs, top_10_values = myIBCF(ratings, Smat)
        movie_rec_ids = [int(mID.replace("m", "")) for mID in movie_recs]
        st.write("Recommended for you:")
        show_recs(movie_rec_ids)

def show_recs(rec_ids):
    i = 0
    for col in st.columns(10):
        if i < len(rec_ids):
            with col.container(height = 500, border = False):
                m_id = rec_ids[i]
                img = Image.open("MovieImages/" + str(m_id) + ".jpg")
                img.thumbnail([200, 200], Image.LANCZOS)
                st.write(img)
                movie_title = movies100[movies100["MovieID"] == m_id]["Title"].values[0]
                st.write(movie_title)
            i += 1

if st.button(label = "Get Recommendations!", type = "primary" ):
    with st.container():
        get_recs(user_ratings_dict)

