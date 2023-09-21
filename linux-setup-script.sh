#!/bin/bash
echo "Setting up the project environment..."

# Create and activate virtual environment
python -m venv venv
source ./venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create .env file
cp sample.env .env

# Run migrations
python manage.py migrate

# Load initial data
python manage.py loaddata data/polls.json
python manage.py loaddata data/users.json
python manage.py loaddata data/vote.json

# Run tests
python manage.py test

# Start the server
echo "Starting the server..."
python manage.py runserver --insecure