import streamlit as st
from streamlit_star_rating import st_star_rating

st.title("🎈Testing out streamlit")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

user_ratings = dict()



def create_star_rating(movie):
    label = movie + " rating"
    amount_of_stars = 5
    default_value = 0
    size = 40
    emoticons = False
    read_only = False
    dark_theme = False
    reset_btn = True

    def function_to_run_on_click(value):
        user_ratings.update({movie: value})
        # st.write(f"**{value}** stars!")

    stars = st_star_rating(label, amount_of_stars, default_value, size, emoticons, read_only, dark_theme,
                           resetButton=False, resetLabel="",
                               customCSS="", on_click=function_to_run_on_click)
    st.write(stars)

create_star_rating("m10")
create_star_rating("m20")

st.write(user_ratings)

