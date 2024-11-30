#!/bin/bash

# Create a virtual environment if not already present
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo "Dependencies installed."

# Set up Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Set up the database
echo "Setting up the database..."
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
echo "Database setup completed."

# Set environment variables for Auth0
echo "Setting environment variables for Auth0..."
export AUTH0_DOMAIN="fsdndp.us.auth0.com"
export API_IDENTIFIER="https://casting-agency-api"
export CLIENT_ID="cVD4RLqh0dgO8UzYvHXibFxyRPkM3hIF"
export CLIENT_SECRET="sa2P4LoMXuqwzrV6XOBwzfZh40VHRsMnqzIh354-NGXc8IIK2KjWTof6UI-QXv9c"
echo "Environment variables set."

echo "Setup complete! You can now run the app with: python app.py"
