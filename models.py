import os
from flask import Flask
from sqlalchemy import Column, String, Integer, Float
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
     
database_name = "casting"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()     
         
# setting up SQLALchemy
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()           

casting = db.Table('casting',
        db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True),
        db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True)
)
    
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Actors
class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    age = Column(String(20))
    gender = Column(String(10))
    movies = db.relationship('Movies', secondary=casting, backref=db.backref('movies'))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {      
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

# Movies
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(20))
    release_date = Column(String(20))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
