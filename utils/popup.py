import streamlit as st  # type: ignore[import-not-found]

from utils.api import (
    get_movie_details,
    get_movie_cast
)

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
