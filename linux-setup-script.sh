#!/bin/bash

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create .env file
cp sample.env .env

# Run migrations
python manage.py migrate

# Load data
python manage.py loaddata data/polls.json
python manage.py loaddata data/users.json

# Load vote data (optional)
# python manage.py loaddata data/vote.json

# Run tests
python manage.py test

# Start server
python manage.py runserver --insecure