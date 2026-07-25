import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
tmdb_api_key = os.getenv("TMDB_API_KEY")


def search_movie(title):
    url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=true"
    headers = {"accept": "application/json", "Authorization": f"Bearer {tmdb_api_key}"}
    response = requests.get(url, headers=headers)

    return response.json()


st.title("Compare Movie Cast and Crew")
col1, col2 = st.columns(2)

with col1:
    title1 = st.text_input("First movie title")
    movies1 = search_movie(title1)
    titles1 = [movie["title"] for movie in movies1["results"]]
    option1 = st.selectbox("First movie", titles1)
    if option1:
        details1 = movies1["results"][titles1.index(option1)]
        st.json(details1)

with col2:
    title2 = st.text_input("Second movie title")
    movies2 = search_movie(title2)
    titles2 = [movie["title"] for movie in movies2["results"]]
    option2 = st.selectbox("Second movie", titles2)
    if option2:
        details2 = movies2["results"][titles2.index(option2)]
        st.json(details2)
