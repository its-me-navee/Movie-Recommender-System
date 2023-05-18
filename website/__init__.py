from flask import Flask
import pickle as pkl
import pandas as pd
from os import path
import requests
from flask_sqlalchemy import SQLAlchemy

movie_dataset = pkl.load(open('movie_dataset.pkl', 'rb'))
# C:\Users\aakib\Documents\ENCRYPTED\PROJECTS\Movie_Recommendation_System\movie_dataset.pkl
db = SQLAlchemy()
DB_NAME = "Movies.db"

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Index = db.Column(db.String(200), nullable = False)
    Action = db.Column(db.Integer, nullable = False)
    Adventure = db.Column(db.Integer, nullable = False)
    Fantasy = db.Column(db.Integer, nullable = False)
    Science = db.Column(db.Integer, nullable = False)
    Fiction = db.Column(db.Integer, nullable = False)
    Crime = db.Column(db.Integer, nullable = False)
    Drama = db.Column(db.Integer, nullable = False)
    Thriller = db.Column(db.Integer, nullable = False)
    Animation = db.Column(db.Integer, nullable = False)
    Family = db.Column(db.Integer, nullable = False)
    Western = db.Column(db.Integer, nullable = False)
    Romance = db.Column(db.Integer, nullable = False)
    Horror = db.Column(db.Integer, nullable = False)
    Mystery = db.Column(db.Integer, nullable = False)
    History = db.Column(db.Integer, nullable = False)
    War = db.Column(db.Integer, nullable = False)
    Music = db.Column(db.Integer, nullable = False)
    Documentary = db.Column(db.Integer, nullable = False)
    Foreign = db.Column(db.Integer, nullable = False)
    Title = db.Column(db.String(200), nullable = False)
    Movieid = db.Column(db.String(200), nullable = False)
    # Posterlink = db.Column(db.String(500), nullable = False)
    Genre = db.Column(db.String(300), nullable = False)
    Popularity = db.Column(db.Float, nullable = False)
    Keywords = db.Column(db.String(300), nullable = True)
    Overview = db.Column(db.String(2000), nullable = True)
    Cast = db.Column(db.String(300), nullable = True)
    Director = db.Column(db.String(200), nullable = True)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kjdshfioejkdsf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.app = app
    db.init_app(app)

    from .home import home
    from .result import result
    # from .result2 import result2

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(result, url_prefix='/')
    # app.register_blueprint(result2, url_prefix='/')


    # create_database(app)

    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            for Id in movie_dataset['index']:
                movieIndex = movie_dataset[movie_dataset.index==Id]['index'].values[0]
                movieTitle = movie_dataset[movie_dataset.index==Id]['title'].values[0]
                movieId = movie_dataset[movie_dataset.index==Id]['movie_id'].values[0]
                movieGenre = movie_dataset[movie_dataset.index==Id]['genres'].values[0]
                moviePopularity = movie_dataset[movie_dataset.index==Id]['popularity'].values[0]
                movieKeywords = movie_dataset[movie_dataset.index==Id]['keywords'].values[0]
                movieOverview = movie_dataset[movie_dataset.index==Id]['overview'].values[0]
                movieCast = movie_dataset[movie_dataset.index==Id]['cast'].values[0]
                movieDirector = movie_dataset[movie_dataset.index==Id]['director'].values[0]
                genreList = []
                genre = ""
                for c in movieGenre:
                    if c == ' ':
                        if genre not in genreList:
                            genreList.append(genre)
                        genre = ""
                    else:
                        genre += str(c)
                if genre not in genreList:
                    genreList.append(genre)
                action, adventure, fantasy, science, fiction, crime, drama, thriller, animation, family, western, romance, horror, mystery, history, war, music, documentary, foreign, tv, movie = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                if 'Action' in genreList:
                    action = 1
                if 'Adventure' in genreList:
                    adventure = 1
                if 'Fantasy' in genreList:
                    fantasy = 1
                if 'Science' in genreList:
                    science = 1
                if 'Fiction' in genreList:
                    fiction = 1
                if 'Crime' in genreList:
                    crime = 1
                if 'Drama' in genreList:
                    drama = 1
                if 'Thriller' in genreList:
                    thriller = 1
                if 'Animation' in genreList:
                    animation = 1
                if 'Family' in genreList:
                    family = 1
                if 'Western' in genreList:
                    western = 1
                if 'Romance' in genreList:
                    romance = 1
                if 'Horror' in genreList:
                    horror = 1
                if 'Mystery' in genreList:
                    mystery = 1
                if 'History' in genreList:
                    history = 1
                if 'War' in genreList:
                    war = 1
                if 'Music' in genreList:
                    music = 1
                if 'Documentary' in genreList:
                    documentary = 1
                if 'Foreign' in genreList:
                    foreign = 1
                newMovie = Movies(Action=action, Adventure=adventure, Fantasy=fantasy, Science=science, Fiction=fiction, Crime=crime, Drama=drama, Thriller=thriller, Animation=animation, Family=family, Western=western, Romance=romance, Horror=horror, Mystery=mystery, History=history, War=war, Music=music, Documentary=documentary, Foreign=foreign, Index=str(movieIndex), Title=movieTitle, Movieid=str(movieId), Genre=movieGenre, Popularity=moviePopularity, Keywords=movieKeywords, Overview=movieOverview, Cast=movieCast, Director=movieDirector)
                with app.app_context():
                    db.session.add(newMovie)
                    db.session.commit()

    return app