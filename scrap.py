import pandas as pd
import numpy as np
import os

# from dash import Dash, dcc, html, Input, Output
# import plotly.express as px
import re

movies = pd.read_csv("movies.dat",
                     sep='::', engine = 'python',
                     encoding="ISO-8859-1", header = None)
movies.columns = ['MovieID', 'Title', 'Genres']

movies100 = movies.iloc[np.random.choice(range(movies.shape[0]), 100, replace=False)]

# print(movies100)
# print(movies.head())
title = movies[movies["MovieID"] == 1]["Title"].values[0]
print(title)

# app = Dash()

# App layout
# app.layout = [html.Div(children='Hello World')]

# load list of 100 cols of S matrix
# input into myICBF() to get a list of 10 recommended movies


if __name__ == "__main__":
    print(" + ".join(np.repeat("st.columns(10)", 10)))
    exec("print(5+5)")
    print(int(movies100["MovieID"].iloc[99]))
    # MovieImage_numbers = os.listdir("MovieImages"

    MovieImage_numbers = [int(n.replace(".jpg", "")) for n in os.listdir("MovieImages")]
    print(MovieImage_numbers)
    movie_image_100 = np.random.choice(MovieImage_numbers, 100, replace=False)
    print(movies[movies["MovieID"].isin(movie_image_100)])


    # app.run(debug=True)