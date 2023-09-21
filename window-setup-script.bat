@echo off
echo Setting up the project environment...

:: Create and activate virtual environment
python -m venv venv
call .\venv\Scripts\activate

:: Install requirements
pip install -r requirements.txt

:: Create .env file
copy sample.env .env

:: Run migrations
python manage.py migrate

:: Load initial data
python manage.py loaddata data/polls.json
python manage.py loaddata data/users.json

:: Uncomment the line below if you want to load vote data (optional)
:: python manage.py loaddata data/vote.json

:: Run tests
python manage.py test

:: Start the server
echo Starting the server...
python manage.py runserver --insecure