

import pickle
import pandas as pd

with open("data/movie_dict.pkl", "rb") as f:
    movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)

with open("data/similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

from utils.api import fetch_poster


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    recommended_movies_ids = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_ids.append(movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return (
        recommended_movies,
        recommended_movies_poster,
        recommended_movies_ids,
    )

def get_movie_titles():
    return movies["title"].values