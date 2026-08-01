# 🎬 Movie Recommendation System

A Content-Based Movie Recommendation System built with Python, Streamlit, and the TMDB (The Movie Database) API. The application recommends similar movies based on user selection and provides rich movie details including posters, ratings, release dates, overviews, and top cast members.

---

## ✨ Features

- **Content-Based Filtering:** Recommends 5 similar movies using cosine similarity metrics on movie features.
- **Interactive UI:** Clean and responsive interface powered by Streamlit.
- **Detailed Modal Popups:** Click on details to view detailed movie information (Overview, Rating, Release Date, Runtime, Genres) and Top Cast.
- **TMDB API Integration:** Real-time fetching of high-resolution movie posters and metadata.

---

## 🛠️ Tech Stack

- **Frontend / UI:** Streamlit
- **Language:** Python 3.x
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning:** Scikit-learn (Cosine Similarity)
- **API:** TMDB API (`requests`)

---

## 📁 Project Structure

```text
Movies_Recommendation/
│-- app.py                     # Main Streamlit web application
│-- main.ipynb                 # Jupyter Notebook for data processing & model building
│-- movie_dict.pkl             # Processed movie dataset (Pickle format)
│-- similarity.pkl             # Precomputed cosine similarity matrix
│-- tmdb_5000_movies.csv       # TMDB Movies dataset
│-- tmdb_5000_credits.csv      # TMDB Credits dataset
│-- .gitignore                 # Files excluded from Version Control
└── README.md                  # Project documentation