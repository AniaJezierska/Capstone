import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies


token = 'authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx1OGdmQks3aHdoZjJNMHpXc1MxcyJ9.eyJpc3MiOiJodHRwczovL2Rldi1pN3YybXR1Yi5ldS5hdXRoMC5jb20vIiwic3ViIjoiZWdSOUpGZTdjQ3J2eWgxWTJkbHJ0bVlRUGFyMTQ2YWdAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MDYzODY0ODMsImV4cCI6MTYwODk3ODQ4MywiYXpwIjoiZWdSOUpGZTdjQ3J2eWgxWTJkbHJ0bVlRUGFyMTQ2YWciLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6W119.u-vTIyLshGC6gQGKfOgZ2JR4sW6jBMqDLiWKV5QicWT9RK1lSFC0JM1r3lFPzuRfLPO33ilZAykIj6Iwutpp-TLu4g0pnpAiOWuJWeDZOTK658FaXUTkJn94TjZX6sKz163Te-TRxT2Fktq6YgG_Lo9j8Vz6qjZQ9RKMyDoQTAsl3RFBlih2-fS4FkF-emsv4LYrzHbq5EwBCa973Ts7eSdyys59QCKXS824ZOXXbIzWIfat0cQ_hoV16UfaHU8iXQ42hbStk6XN_Fp_v6zCBjoLu3CC8DnEl4qeSRN9LqNHouh3GZNAxyi15p1zoqtUKLHaPf3Enxrn9E_rt8OUIA'
header = 'Bearer' + ' ' + token
auth_header = {'Authorization': header}


class Casting_Test(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://{}/{}".format('localhost:8081', self.database_name)

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer',
            'Token': token}

        self.actor = Actors(
            name='Amy',
            age='50',
            gender='Female'
        )

        self.movie = Movies(
            title='Grinch',
            release_date='25'
        )

        self.new_actor = {
            'name': 'Jason',
            'age': '32',
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'Holiday',
            'release_date': '28'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.actor.insert()
        self.movie.insert()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        response = self.client().get('/actors', headers=auth_header)
        data = response.json
        self.assertEqual(response.status_code, 200)

    def test_create_actor(self):
        response = self.client().post('/actors',  headers=auth_header, json=self.new_actor)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'successful')

    def test_delete_actor(self):
        response = self.client().delete('/actors/20', headers=auth_header)
        data = response.json
        actor = Actors.query.filter(Actors.id == 2).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(actor, None)

    def test_get_movies(self):
        response = self.client().get('/movies', headers=auth_header)
        data = response.json
        self.assertEqual(response.status_code, 200)

    def test_create_movie(self):
        response = self.client().\
            post('/movies', headers=auth_header, json=self.new_movie)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'successful')

    def test_delete_movie(self):
        response = self.client().delete('/movies/20', headers=auth_header)
        data = response.json
        movie = Movies.query.filter(Movies.id == 2).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(movie, None)

    def test_404_delete_actor_doesnt_exist(self):
        response = self.client().delete('/actors/1000', headers=auth_header)
        data = response.json
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status'], 'not found')

    def test_404_delete_movie_doesnt_exist(self):
        response = self.client().delete('/movies/1000', headers=auth_header)
        data = response.json
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status'], 'not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
