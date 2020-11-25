import os
from flask import Flask, request, abort, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # set up CORS. Allow '*' for origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        # list of http request header values the server will allow
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        # list of HTTP request types allowed
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/')
    def healthy():
        return jsonify({
          'status': 'logged in'
        })

    # Actors endpoints

    #  Create an endpoint to handle GET requests for actors,
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors_query = Actors.query.all()

        if actors_query is None:
            abort(404)

        actors = [actor.format() for actor in actors_query]

        return jsonify({
          'status': 'successful',
          'actors': actors
          }), 200

    #   Create an endpoint to POST a new actor.
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(payload):

        body = request.get_json()

        new_actor = Actors(
          name=body.get('name', ''),
          age=body.get('age', ''),
          gender=body.get('gender', '')
        )

        new_actor.insert()

        return jsonify({
          'status': 'successful'
        }), 200

    #   Create an endpoint to DELETE an actor.
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, id):
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
          'status': 'succesful'
        }), 200

    #   Create an endpoint to PATCH
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def edit_actor(payload, id):
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        if actor is None:
            abort(404)

        body = request.get_json()

        actor.name = body.get('name', '')
        actor.age = body.get('age', '')
        actor.gender = body.get('gender', '')

        actor.update()

        return jsonify({
          'status': 'successful'
        }), 200

    # Movies endpoints

    #  Create an endpoint to handle GET requests for movies,
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies_query = Movies.query.all()

        movies = [movie.format() for movie in movies_query]

        return jsonify({
          'status': 'successful',
          'movies': movies
        }), 200

    #   Create an endpoint to POST a new movie.
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movie')
    def create_movie(payload):
        body = request.get_json()
        new_movie = Movies(
          title=body.get('title', ''),
          release_date=body.get('release_date', '')
        )

        new_movie.insert()

        return jsonify({
          'status': 'successful'
        }), 200

    #   Create an endpoint to DELETE an actor.
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, id):
        movie = Movies.query.filter(Movies.id == id).one_or_none()
        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
          'status': 'successful'
        }), 200

    #   Create an endpoint to PATCH
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def edit_movie(payload, id):
        movie = Movies.query.filter(Movies.id == id).one_or_none()
        if movie is None:
            abort(404)

        body = request.get_json()

        movie.title = body.get('title', '')
        movie.release_date = body.get('release_date', '')

        movie.update()

        return jsonify({
          'status': 'successful'
        }), 200

    # error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessed"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    return app

app = create_app()
