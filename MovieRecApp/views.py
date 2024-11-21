import os
import pickle
from django.shortcuts import render
from django.conf import settings
import pandas as pd

# Load the cosine similarity matrix (ensure the path is correct)
cosine_sim_df = None
try:
    with open(os.path.join(settings.BASE_DIR, 'cosine_sim.pkl'), 'rb') as file:
        cosine_sim_df = pickle.load(file)
    print("Cosine similarity matrix loaded successfully!")
except FileNotFoundError:
    print("Error: cosine_sim.pkl file not found.")
except Exception as e:
    print(f"Error loading the cosine similarity matrix: {e}")

# Function to get similar movies
def get_similar_movies(movie_title, cosine_sim_df):
    if movie_title in cosine_sim_df.index:
        idx = cosine_sim_df.index.get_loc(movie_title)
        sim_scores = list(enumerate(cosine_sim_df.iloc[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_movies = [cosine_sim_df.index[i] for i, _ in sim_scores[1:6]]
        return top_movies
    else:
        return ["Movie not found in dataset."]


# Home view to handle the form submission
def home(request):
    recommendations = None
    movie_title = None
    
    if request.method == 'POST':
        movie_title = request.POST.get('movie_title')
        print(f"Received movie title: {movie_title}")  # Debugging line

        # Print first 10 movie titles from the dataset
        print("Sample movie titles in the dataset:")
        print(cosine_sim_df.index[:10])  # Prints the first 10 movie titles from the dataset

        recommendations = get_similar_movies(movie_title, cosine_sim_df)
        print(f"Recommendations: {recommendations}")  # Debugging line
    
    return render(request, 'MovieRecApp/home.html', {'recommendations': recommendations, 'movie_title': movie_title})

# Function to display the recommendations (if needed for a specific template)
def recommend_movies(request):
    recommendations = None
    if request.method == 'POST':
        movie_title = request.POST.get('movie_title')
        recommendations = get_similar_movies(movie_title, cosine_sim_df)
    
    return render(request, 'recommend.html', {'recommendations': recommendations})
