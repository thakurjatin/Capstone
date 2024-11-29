from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from auth import AuthError, requires_auth

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/moviesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def format(self):
        return {"id": self.id, "title": self.title, "release_date": self.release_date.isoformat()}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def format(self):
        return {"id": self.id, "name": self.name, "age": self.age, "gender": self.gender}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Routes
@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(jwt):
    movies = Movie.query.all()
    return jsonify({"success": True, "movies": [movie.format() for movie in movies]}), 200


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(jwt):
    actors = Actor.query.all()
    return jsonify({"success": True, "actors": [actor.format() for actor in actors]}), 200


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movie(jwt):
    data = request.get_json()
    title = data.get('title')
    release_date = data.get('release_date')
    if not title or not release_date:
        abort(400)
    movie = Movie(title=title, release_date=release_date)
    movie.insert()
    return jsonify({"success": True, "movie": movie.format()}), 201


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movie(jwt, movie_id):
    data = request.get_json()
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    movie.title = data.get('title', movie.title)
    movie.release_date = data.get('release_date', movie.release_date)
    movie.update()
    return jsonify({"success": True, "movie": movie.format()}), 200


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    movie.delete()
    return jsonify({"success": True, "deleted": movie_id}), 200

# Error Handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Resource not found"}), 404


@app.errorhandler(403)
def forbidden(error):
    return jsonify({"success": False, "error": 403, "message": "Permission not found"}), 403


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({"success": False, "error": error.status_code, "message": error.error['description']}), error.status_code


if __name__ == '__main__':
    app.run(debug=True)
