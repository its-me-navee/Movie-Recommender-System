import numpy as np
import pandas as pd
import pickle as pkl
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from os import path

movie_dataset = pd.read_csv( 'movies_data.csv')
movie_dataset.dropna(inplace=True)

selected_features = ['genres', 'keywords', 'overview', 'cast', 'director']

combined_features = movie_dataset['genres'] + movie_dataset['keywords'] + movie_dataset['overview'] + movie_dataset['cast'] + movie_dataset['director']

vectorizer = TfidfVectorizer()
combined_features = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(combined_features)


if not path.exists('website/' + 'model.pkl'):
    pkl.dump(similarity, open('model.pkl', 'wb'))
    pkl.dump(movie_dataset, open('movie_dataset.pkl', 'wb'))

