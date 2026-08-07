
# pyright: reportMissingImports=false
import streamlit as st

from utils.recommender import recommend, get_movie_titles

from utils.popup import show_movie_popup



# ------------------ MAIN APP UI ------------------
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")

with st.sidebar:

    st.title("About")

    st.write("""
    This project recommends movies using
    Content-Based Filtering.

    Dataset :
    TMDB 5000 Movies

    Developed by:
    Insha Rani
    """)



# Session state initialization (Very Important for persistence)
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

selected_movie_name = st.selectbox(
    "Select a Movie",
    get_movie_titles()
)

if st.button("Recommend"):
    loading = st.empty()

    loading.info("⏳ Please wait, we are finding best movies for you...")

    names, posters, ids = recommend(selected_movie_name)
    st.session_state.recommendations = {
        "names": names,
        "posters": posters,
        "ids": ids,
    }
    loading.empty()

    st.success("Recommendations ready!")


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