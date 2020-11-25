import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies


token = ''
expired_token = ''
permissions_not_included_token = ''
expired_header = 'Bearer' + ' ' + expired_token
permission_not_found = 'Bearer' + permissions_not_included_token
header = 'Bearer' + ' ' + token
expired_auth_header = {'Authorization': expired_header}
auth_header = {'Authorization': header}


class Casting_Test(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization": "Bearer {}".format(token)
        }

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
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_create_actor(self):
        response = self.client().post('/actors',  headers=auth_header, json=self.new_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'successful')

    def test_delete_actor(self):
        response = self.client().delete('/actors/20', headers=auth_header)
        data = json.loads(response.data)
        actor = Actors.query.filter(Actors.id == 2).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(actor, None)

    def test_get_movies(self):
        response = self.client().get('/movies', headers=auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_create_movie(self):
        response = self.client().\
            post('/movies', headers=auth_header, json=self.new_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'successful')

    def test_delete_movie(self):
        response = self.client().delete('/movies/20', headers=auth_header)
        data = json.loads(response.data)
        movie = Movies.query.filter(Movies.id == 2).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(movie, None)

    def test_404_delete_actor_doesnt_exist(self):
        response = self.client().delete('/actors/1000', headers=auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status'], 'not found')

    def test_404_delete_movie_doesnt_exist(self):
        response = self.client().delete('/movies/1000', headers=auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status'], 'not found')

    def test_401_unauthorised(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['status'], 'unauthorised')

    def test_403_permission_not_found(self):
        response = self.client().get('/actors', headers=expired_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['status'], 'unauthorised')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    
