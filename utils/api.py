import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


# 1. Safe Poster Fetching
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except requests.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# 2. Movie Details Fetching
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    return response.json()


# 3. Movie Cast Fetching
def get_movie_cast(movie_id):
    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    return data.get("cast", [])[:6]
