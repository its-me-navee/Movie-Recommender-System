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

result = Blueprint('result', __name__)

def recommended_movies_genre(movie_genre):
    recommended_movie_posters = []
    if movie_genre == "Action":
        result = Movies.query.filter_by(Action=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Adventure":
        result = Movies.query.filter_by(Adventure=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Fantasy":
        result = Movies.query.filter_by(Fantasy=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Science":
        result = Movies.query.filter_by(Science=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Fiction":
        result = Movies.query.filter_by(Fiction=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Crime":
        result = Movies.query.filter_by(Crime=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Drama":
        result = Movies.query.filter_by(Drama=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Thriller":
        result = Movies.query.filter_by(Thriller=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Animation":
        result = Movies.query.filter_by(Animation=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Family":
        result = Movies.query.filter_by(Family=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Western":
        result = Movies.query.filter_by(Western=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Romance":
        result = Movies.query.filter_by(Romance=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Horror":
        result = Movies.query.filter_by(Horror=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Mystery":
        result = Movies.query.filter_by(Mystery=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "History":
        result = Movies.query.filter_by(History=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "War":
        result = Movies.query.filter_by(War=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Music":
        result = Movies.query.filter_by(Music=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Documentary":
        result = Movies.query.filter_by(Documentary=1).order_by(Movies.Popularity.desc()).all()
    if movie_genre == "Foreign":
        result = Movies.query.filter_by(Foreign=1).order_by(Movies.Popularity.desc()).all()
    for item in result:
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=11c0a87689a02c4a51143526d9c86c87&language=en-US'.format(item.Movieid))
        data = response.json()
        if not data['poster_path']:
            continue
        recommended_movie_posters.append("https://image.tmdb.org/t/p/w500/" + data['poster_path'])
        if len(recommended_movie_posters)==12:
            break
    return recommended_movie_posters

def recommended_movies(movie_name, movie_genre):
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
        idx1 = 0
        if movie_genre == "Action" and res.Action==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Adventure" and res.Adventure==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Fantasy" and res.Fantasy==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Science" and res.Science==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Fiction" and res.Fiction==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Crime" and res.Crime==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Drama" and res.Drama==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Thriller" and res.Thriller==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Animation" and res.Animation==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Family" and res.Family==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Western" and res.western==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Romance" and res.Romance==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Horror" and res.Horror==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Mystery" and res.Mystery==1:
            idx1 = int(res.Movieid)
        if movie_genre == "History" and res.History==1:
            idx1 = int(res.Movieid)
        if movie_genre == "War" and res.War==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Music" and res.Music==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Documentary" and res.Documentary==1:
            idx1 = int(res.Movieid)
        if movie_genre == "Foreign" and res.Foreign==1:
            idx1 = int(res.Movieid)
        if idx1 != 0:
            response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=11c0a87689a02c4a51143526d9c86c87&language=en-US'.format(idx1))
            data = response.json()
            if not data['poster_path']:
                continue
            recommended_movie_posters.append("https://image.tmdb.org/t/p/w500/" + data['poster_path'])
        if len(recommended_movie_posters)==12:
            break
    return recommended_movie_posters

@result.route('/Adventure', methods=['GET', 'POST'])
def Adventurepage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Adventure")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Adventure", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Adventure Movies")
    else:
        if request.method == 'POST':
            movie_name = request.form.get('movie_name')
            matches = process.extract(movie_name, movie_titles, limit = 1)
            if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
                movie_name = matches[0][0]
                print(movie_name)
                recommended_movie_posters = recommended_movies(movie_name, "Adventure")
                return render_template("result3.html", genre_name="Adventure", name = movie_name, movie_list = recommended_movie_posters)
            else:
                print("Not found")
                return render_template("error.html", name=movie_name)
        else:
            return render_template("result2.html")
    
@result.route('/Action', methods=['GET', 'POST'])
def Actionpage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Action")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Action", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Action Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Action")
            return render_template("result3.html", genre_name="Action", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
 
    
@result.route('/Fantasy', methods=['GET', 'POST'])
def Fantasypage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Fantasy")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Fantasy", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Fantasy Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Fantasy")
            return render_template("result3.html", genre_name="Fantasy", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Science', methods=['GET', 'POST'])
def Sciencepage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Science")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Science", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Science Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Science")
            return render_template("result3.html", genre_name="Science", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Fiction', methods=['GET', 'POST'])
def Fictionpage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Fiction")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Fiction", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Fiction Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Fiction")
            return render_template("result3.html", genre_name="Fiction", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
        
@result.route('/Crime', methods=['GET', 'POST'])
def Crimepage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Crime")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Crime", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Crime Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Crime")
            return render_template("result3.html", genre_name="Crime", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Drama', methods=['GET', 'POST'])
def Dramapage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Drama")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Drama", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Drama Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Drama")
            return render_template("result3.html", genre_name="Drama", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Thriller', methods=['GET', 'POST'])
def Thrillerpage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Thriller")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Thriller", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Thriller Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Thriller")
            return render_template("result3.html", genre_name="Thriller", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Animation', methods=['GET', 'POST'])
def Animationpage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Animation")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Animation", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Animation Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Animation")
            return render_template("result3.html", genre_name="Animation", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Family', methods=['GET', 'POST'])
def Familypage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Family")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Family", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Family Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Family")
            return render_template("result3.html", genre_name="Family", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Western', methods=['GET', 'POST'])
def Westernpage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Western")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Western", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Western Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Western")
            return render_template("result3.html", genre_name="Western", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Romance', methods=['GET', 'POST'])
def Romancepage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Romance")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Romance", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Romance Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Romance")
            return render_template("result3.html", genre_name="Romance", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Horror', methods=['GET', 'POST'])
def Horrorpage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Horror")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Horror", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Horror Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Horror")
            return render_template("result3.html", genre_name="Horror", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Mystery', methods=['GET', 'POST'])
def Mysterypage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Mystery")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Mystery", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Mystery Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Mystery")
            return render_template("result3.html", genre_name="Mystery", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
        
@result.route('/History', methods=['GET', 'POST'])
def Historypage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("History")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "History", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="History Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "History")
            return render_template("result3.html", genre_name="History", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/War', methods=['GET', 'POST'])
def Warpage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("War")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "War", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="War Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "War")
            return render_template("result3.html", genre_name="War", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Music', methods=['GET', 'POST'])
def Musicpage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Music")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Music", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Music Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Music")
            return render_template("result3.html", genre_name="Music", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Documentary', methods=['GET', 'POST'])
def Documentarypage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Documentary")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Documentary", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Documentary Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Documentary")
            return render_template("result3.html", genre_name="Documentary", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    
@result.route('/Foreign', methods=['GET', 'POST'])
def Foreignpage():
    if request.method == 'GET':
        recommended_movie_posters = recommended_movies_genre("Foreign")
        if len(recommended_movie_posters) > 0:
            return render_template("result2.html", genre = "Foreign", movie_list = recommended_movie_posters)
        else:
            return render_template("error.html", name="Foreign Movies")
    else:
        movie_name = request.form.get('movie_name')
        matches = process.extract(movie_name, movie_titles, limit = 1)
        if nltk.edit_distance(movie_name, matches[0][0]) <= 3:
            movie_name = matches[0][0]
            print(movie_name)
            recommended_movie_posters = recommended_movies(movie_name, "Foreign")
            return render_template("result3.html", genre_name="Foreign", name = movie_name, movie_list = recommended_movie_posters)
        else:
            print("Not found")
            return render_template("error.html", name=movie_name)
    