from flask import Blueprint, render_template, request
import numpy as np
import pandas as pd
from website import db
from website import Movies
from fuzzywuzzy import process
import nltk
import pickle as pkl
import requests


similarity = pkl.load(open('model.pkl', 'rb'))
movie_dataset = pkl.load(open('movie_dataset.pkl', 'rb'))
movie_titles = movie_dataset['title'].tolist()

home = Blueprint('home', __name__)

def recommended_movies(movie_name):
    print(movie_name)
    result = Movies.query.filter_by(Title=movie_name).first()
    index_of_the_movie = int(result.Index)
    similarity_score = similarity[index_of_the_movie]
    similarity_score = list(enumerate(similarity_score))
    similarity_score.sort(key = lambda x:x[1], reverse = True)
    recommended_movie_posters = []
    for [idx, similar_score] in similarity_score:
        res = Movies.query.filter_by(Index=str(idx)).first()
        if not res:
            continue
        idx1 = int(res.Movieid)
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=11c0a87689a02c4a51143526d9c86c87&language=en-US'.format(idx1))
        data = response.json()
        if not data['poster_path']:
            continue
        recommended_movie_posters.append("https://image.tmdb.org/t/p/w500/" + data['poster_path'])
        if len(recommended_movie_posters)==12:
            break
    return recommended_movie_posters

@home.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST' and len(request.form.get('movie_name')) > 0:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            recommended_movie_posters = recommended_movies(movie_name)
            return render_template("result1.html", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    else:
        return render_template("home.html")
