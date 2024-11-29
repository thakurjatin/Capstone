import unittest
from flask import Flask
from app import app, create_app
from models import db, Movie, Actor
import os

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.assistant_jwt = os.getenv('ASSISTANT_JWT', 'your_assistant_jwt_here')
        self.producer_jwt = os.getenv('PRODUCER_JWT', 'your_producer_jwt_here')

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
     def test_get_movies_as_assistant(self):
        """Test GET /movies with assistant role."""
        headers = {"Authorization": f"Bearer {self.assistant_jwt}"}
        res = self.client().get('/movies', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_post_movies_without_permission(self):
        """Test POST /movies with insufficient permissions."""
        headers = {"Authorization": f"Bearer {self.assistant_jwt}"}
        payload = {"title": "New Movie"}
        res = self.client().post('/movies', headers=headers, json=payload)
        self.assertEqual(res.status_code, 403)

if __name__ == "__main__":
    unittest.main()