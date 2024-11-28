#!/bin/bash

# Create a virtual environment if not already present
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo "Dependencies installed."

# Set up database
export FLASK_APP=app.py
export FLASK_ENV=development
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
echo "Database setup completed."

# Set environment variables
echo "Setting environment variables"
export AUTH0_DOMAIN='your-auth0-domain'
export API_IDENTIFIER='your-api-identifier'
echo "Environment variables set."

echo "Setup complete! You can now run the app with: python app.py"
