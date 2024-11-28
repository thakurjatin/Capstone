from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from models import db, Movie, Actor
from auth import requires_auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/casting_agency'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)

# Route to get all actors
@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    actors = Actor.query.all()
    return jsonify({
        'success': True,
        'actors': [actor.format() for actor in actors]
    })

# Route to get all movies
@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    movies = Movie.query.all()
    return jsonify({
        'success': True,
        'movies': [movie.format() for movie in movies]
    })

# Route to create a new actor
@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):
    body = request.get_json()
    try:
        new_actor = Actor(
            name=body['name'],
            age=body['age'],
            gender=body['gender']
        )
        new_actor.insert()
        return jsonify({
            'success': True,
            'actor': new_actor.format()
        })
    except Exception as e:
        abort(400)

# Route to create a new movie
@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):
    body = request.get_json()
    try:
        new_movie = Movie(
            title=body['title'],
            release_date=body['release_date']
        )
        new_movie.insert()
        return jsonify({
            'success': True,
            'movie': new_movie.format()
        })
    except Exception as e:
        abort(400)

# Route to update an existing actor
@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, id):
    actor = Actor.query.get(id)
    if actor is None:
        abort(404)
    body = request.get_json()
    try:
        if 'name' in body:
            actor.name = body['name']
        if 'age' in body:
            actor.age = body['age']
        if 'gender' in body:
            actor.gender = body['gender']
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    except Exception as e:
        abort(400)

# Route to update an existing movie
@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, id):
    movie = Movie.query.get(id)
    if movie is None:
        abort(404)
    body = request.get_json()
    try:
        if 'title' in body:
            movie.title = body['title']
        if 'release_date' in body:
            movie.release_date = body['release_date']
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })
    except Exception as e:
        abort(400)

# Route to delete an actor
@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, id):
    actor = Actor.query.get(id)
    if actor is None:
        abort(404)
    try:
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': id
        })
    except Exception as e:
        abort(400)

# Route to delete a movie
@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, id):
    movie = Movie.query.get(id)
    if movie is None:
        abort(404)
    try:
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': id
        })
    except Exception as e:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True)
