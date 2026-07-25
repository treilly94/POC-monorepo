import os

import pandas as pd
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


def get_credits(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {"accept": "application/json", "Authorization": f"Bearer {tmdb_api_key}"}
    response = requests.get(url, headers=headers)

    return response.json()


st.title("Compare Movie Cast and Crew")
col1, col2 = st.columns(2)

credits1 = None
credits2 = None

with col1:
    title1 = st.text_input("First movie title")
    movies1 = search_movie(title1)
    titles1 = [movie["title"] for movie in movies1["results"]]
    option1 = st.selectbox("First movie", titles1)
    if option1:
        details1 = movies1["results"][titles1.index(option1)]
        credits1 = get_credits(details1["id"])

with col2:
    title2 = st.text_input("Second movie title")
    movies2 = search_movie(title2)
    titles2 = [movie["title"] for movie in movies2["results"]]
    option2 = st.selectbox("Second movie", titles2)
    if option2:
        details2 = movies2["results"][titles2.index(option2)]
        credits2 = get_credits(details2["id"])

if credits1 and credits2:
    st.subheader("Common Cast")
    cast1 = pd.DataFrame(credits1["cast"])[["name", "character"]]
    cast2 = pd.DataFrame(credits2["cast"])[["name", "character"]]
    common_cast = cast1.merge(
        cast2, on="name", how="inner", suffixes=(f" {option1}", f" {option2}")
    )
    st.write(common_cast)

    st.subheader("Common Crew")
    crew1 = pd.DataFrame(credits1["crew"])[["name", "job"]]
    crew2 = pd.DataFrame(credits2["crew"])[["name", "job"]]
    common_crew = crew1.merge(
        crew2, on="name", how="inner", suffixes=(f" {option1}", f" {option2}")
    )
    st.write(common_crew)
