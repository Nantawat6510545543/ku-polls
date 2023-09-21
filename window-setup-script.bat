@REM Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

@REM Install requirements
pip install -r requirements.txt

@REM Create .env file
copy sample.env .env

@REM Run migrations
python manage.py migrate

@REM Load data
python manage.py loaddata data/polls.json
python manage.py loaddata data/users.json

@REM Load vote data (optional)
@REM python manage.py loaddata data/vote.json

@REM Run tests
python manage.py test

@REM Start server
python manage.py runserver --insecure