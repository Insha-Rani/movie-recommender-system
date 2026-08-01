import pandas as pd
import pickle
import requests
import streamlit as st

API_KEY = "9efbd382170df994adff9c7aa66a79b1"


# 1. Safe Poster Fetching
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass
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


# ------------------ STREAMLIT POPUP DIALOG ------------------
@st.dialog("Movie Details")
def show_movie_popup(movie_id):
    with st.spinner("Please Wait We Are Loading Details..."):
        details = get_movie_details(movie_id)
        cast = get_movie_cast(movie_id)

    st.header(details.get("title", "Movie Details"))

    col_img, col_info = st.columns([1, 2])
    with col_img:
        poster_path = details.get("poster_path")
        if poster_path:
            st.image(f"https://image.tmdb.org/t/p/w500{poster_path}")
    with col_info:
        st.write(f"⭐ **Rating:** {details.get('vote_average', 'N/A')}/10")
        st.write(f"📅 **Release Date:** {details.get('release_date', 'N/A')}")
        st.write(f"⏱️ **Runtime:** {details.get('runtime', 'N/A')} mins")
        genres = [g["name"] for g in details.get("genres", [])]
        st.write(f"🎭 **Genres:** {', '.join(genres)}")

    st.subheader("📖 Overview")
    st.write(details.get("overview", "No description available."))

    st.divider()

    st.subheader("👥 Top Cast")
    if cast:
        cast_cols = st.columns(min(len(cast), 6))
        for idx, actor in enumerate(cast):
            with cast_cols[idx]:
                profile_path = actor.get("profile_path")
                if profile_path:
                    st.image(f"https://image.tmdb.org/t/p/w185{profile_path}")
                else:
                    st.write("🖼️ No Photo")
                st.caption(f"**{actor.get('name')}**")
                st.caption(f"*{actor.get('character')}*")


# ------------------ MAIN APP UI ------------------
st.title("Movie Recommendation System")

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))


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


# Session state initialization (Very Important for persistence)
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

selected_movie_name = st.selectbox(
    "Select a movie:", movies["title"].values
)

if st.button("Recommend"):
    names, posters, ids = recommend(selected_movie_name)
    st.session_state.recommendations = {
        "names": names,
        "posters": posters,
        "ids": ids,
    }

# Display recommendations if available in session state
if st.session_state.recommendations is not None:
    rec = st.session_state.recommendations
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(rec["posters"][i])
            st.caption(rec["names"][i])
            if st.button(" Details", key=f"details_btn_{i}"):
                show_movie_popup(rec["ids"][i])