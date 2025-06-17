import pandas as pd
import requests
import streamlit as st
import pickle

def get_imdb_id_from_title(title):
    api_key = "82aca5b7"
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data.get('Response') == 'True':
        return data['imdbID']
    else:
        return None

def fetch_poster(imdb_id):
    # Use OMDB API with your key
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=82aca5b7"
    data = requests.get(url).json()
    
    # Check if poster exists in response
    if 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster']  # OMDB returns full URL directly
    else:
        # Return a placeholder image if no poster found
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        # Assuming your movie_dict contains IMDB IDs in the format 'tt3896198'
        imdb_id = get_imdb_id_from_title(movies.iloc[i[0]].title) 
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(imdb_id))

    return recommended_movies, recommended_posters

# Load data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

# import streamlit.components.v1 as components

# imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# imageUrls = [
#     fetch_poster(get_imdb_id_from_title("Inception")),
#     fetch_poster(get_imdb_id_from_title("Tangled")),
#     fetch_poster(get_imdb_id_from_title("The Long Ranger")),
#     fetch_poster(get_imdb_id_from_title("Flipper")),
#     fetch_poster(get_imdb_id_from_title("Accidental Love")),
#     fetch_poster(get_imdb_id_from_title("W.")),
#     fetch_poster(get_imdb_id_from_title("Taken")),
#     fetch_poster(get_imdb_id_from_title("The Help")),
#     fetch_poster(get_imdb_id_from_title("Ride Along")),
#     fetch_poster(get_imdb_id_from_title("The Untouchables")),
#     fetch_poster(get_imdb_id_from_title("Chocolat")),
#     fetch_poster(get_imdb_id_from_title("The Omen")),
#     fetch_poster(get_imdb_id_from_title("Tombstone"))
#     ]


# imageCarouselComponent(imageUrls=imageUrls, height=200)

selected_movie = st.selectbox(
    'Select your fav movie', movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for col, name, poster in zip([col1, col2, col3, col4, col5], 
                               recommended_movie_names, 
                               recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)
