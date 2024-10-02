from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Load datasets
movies = pd.read_csv('data/movies.csv')
ratings = pd.read_csv('data/ratings.csv')

# Recommendation function based on user input
def get_recommendations(movie_name, num_recommendations=5):
    movie = movies[movies['title'].str.contains(movie_name, case=False, na=False)]
    if movie.empty:
        return []

    movie_id = movie.iloc[0]['movieId']
    movie_ratings = ratings[ratings['movieId'] == movie_id]
    
    # Simple logic: Recommend movies that other users who liked this movie have rated highly
    similar_users = ratings[ratings['userId'].isin(movie_ratings['userId'])]
    top_movies = similar_users.groupby('movieId').rating.mean().sort_values(ascending=False).head(num_recommendations)
    
    recommendations = movies[movies['movieId'].isin(top_movies.index)]
    return recommendations['title'].tolist()

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Recommendation result route
@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie']
    recommendations = get_recommendations(movie_name)
    if recommendations:
        return render_template('result.html', movie_name=movie_name, recommendations=recommendations)
    else:
        return render_template('result.html', movie_name=movie_name, recommendations=None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from environment, default to 5000
    app.run(host='0.0.0.0', port=port)  # Bind to 0.0.0.0 and the environment port
