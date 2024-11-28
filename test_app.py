import unittest
from app import app
from models import db, Movie, Actor

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client

    # Test getting actors
    def test_get_actors(self):
        response = self.client().get('/actors')
        self.assertEqual(response.status_code, 200)

    # Test getting movies
    def test_get_movies(self):
        response = self.client().get('/movies')
        self.assertEqual(response.status_code, 200)

    # Test creating an actor
    def test_create_actor(self):
        response = self.client().post('/actors', json={
            'name': 'John Doe',
            'age': 30,
            'gender': 'Male'
        })
        self.assertEqual(response.status_code, 200)

    # Test creating a movie
    def test_create_movie(self):
        response = self.client().post('/movies', json={
            'title': 'Movie Title',
            'release_date': '2024-11-01'
        })
        self.assertEqual(response.status_code, 200)

    # Additional tests for error handling and RBAC go here...
