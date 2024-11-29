# Casting Agency API
The Casting Agency API is a backend system for a casting agency to manage movies and actors. It supports role-based access control (RBAC) with roles for Assistant, Director, and Producer.
________________________________________
## Motivation
The goal of this project is to provide a scalable backend API for managing movies and actors. It demonstrates:
•	Implementation of Role-Based Access Control (RBAC) using Auth0.
•	Secure access to endpoints with JWT authentication.
•	Proper API design, error handling, and testing.
________________________________________
## Live API
•	The API is hosted on Heroku/Render.
•	Authentication is required to access the API. Follow the instructions in the Authentication section to configure JWTs.
________________________________________
## Setup and Installation
### Dependencies
•	Python 3.8 or higher
•	Flask
•	PostgreSQL
•	Auth0
•	Required libraries (listed in requirements.txt)

## Local Development
1.	Clone the Repository
    bash
    git clone https://github.com/thakurjatin/Capstone.gitcd casting-agency
2.	Install Dependencies
    bash
    pip install -r requirements.txt
3.	Set Up the Database
    o	Install PostgreSQL.
    o	Create a database named moviesdb and set up tables by running:
    bash
    export FLASK_APP=app.py
    flask db upgrade
4.	Configure Environment Variables Create a .env file:
    bash
    AUTH0_DOMAIN=your-auth0-domain
    API_AUDIENCE=your-api-audience
    ALGORITHMS=['RS256']
    ASSISTANT_JWT=your-assistant-jwt
    PRODUCER_JWT=your-producer-jwt

5.	Run the Application
    bash
    export FLASK_ENV=development
    flask run
6.	Access the API
    o	Local URL: http://127.0.0.1:5000
________________________________________
## Authentication
### Auth0 Configuration
    1.	Log in to Auth0.
    2.	Create an application and configure the API audience.
    3.	Define roles:
    o	Assistant: Can view movies and actors.
    o	Producer: Full access to movies and actors.
    4.	Assign permissions:
    o	get:movies, get:actors, post:movies, patch:movies, delete:movies.
    Using JWTs
    •	Generate JWTs from the Auth0 dashboard or an Auth0-enabled client.
    •	Include the token in the Authorization header as Bearer <token>.
________________________________________
## Endpoints
### GET /movies
    •	Permissions: get:movies
    •	Response:
    {
      "success": true,
      "movies": [
        {"id": 1, "title": "Inception", "release_date": "2010-07-16"}
      ]
    }
### GET /actors
    •	Permissions: get:actors
    •	Response:
    {
      "success": true,
      "actors": [
        {"id": 1, "name": "Leonardo DiCaprio", "age": 47, "gender": "Male"}
      ]
    }
### POST /movies
    •	Permissions: post:movies
    •	Request Body:
    {"title": "Tenet", "release_date": "2020-08-26"}
    •	Response:
    {
      "success": true,
      "movie": {"id": 2, "title": "Tenet", "release_date": "2020-08-26"}
    }
### PATCH /movies/<id>
    •	Permissions: patch:movies
    •	Response:
    {
      "success": true,
      "movie": {"id": 2, "title": "Tenet Updated", "release_date": "2020-08-26"}
    }
### DELETE /movies/<id>
    •	Permissions: delete:movies
    •	Response:
    {
      "success": true,
      "deleted": 2
    }
________________________________________
## Error Handling
    Status Code	Description
    400	Bad request
    401	Unauthorized
    403	Forbidden
    404	Resource not found
________________________________________
## Testing
    1.	Set Up Test Configuration
    o	Configure a test database in test_config.py.
    o	Update JWTs for each role in test_app.py.
    2.	Run Tests
    python -m unittest test_app.py

