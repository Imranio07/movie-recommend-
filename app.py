import pickle
import pandas as pd
import streamlit as st
import requests

# Load data
movies_df = pd.read_pickle('movie_list.pkl')
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    # Find index of selected movie
    movie_index = movies_df[movies_df['title'] == movie].index[0]

    # Calculate distances between selected movie and others
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])

    # Get names and posters of 5 similar movies
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies_df.iloc[i[0]].get('movie_id')
        if movie_id:
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies_df.iloc[i[0]].title)
        else:
            recommended_movie_posters.append(None)
            recommended_movie_names.append("Movie ID not found")

    return recommended_movie_names, recommended_movie_posters

# Display interface
st.header('Movie Recommender System')

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies_df['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Use st.columns instead of deprecated st.beta_columns
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            if recommended_movie_posters[i]:
                st.image(recommended_movie_posters[i])
