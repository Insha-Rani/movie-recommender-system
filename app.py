import streamlit as st
import pickle
import pandas as pd

# Page ka title set karein
st.title('Movie Recommendation System')

# 1. Saved files ko load karein
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# 2. Recommendation logic function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # Top 5 similar movies nikalna
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# 3. Streamlit UI Elements
# Dropdown menu banayein jisme saari movies ke naam hon
selected_movie_name = st.selectbox(
    'Apni pasand ki movie select karein:',
    movies['title'].values
)

# Recommend button banayein
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    
    st.write('### Aapke liye Top 5 Movies:')
    # Saare names ko screen par display karein
    for current_movie in recommendations:
        st.subheader(current_movie)