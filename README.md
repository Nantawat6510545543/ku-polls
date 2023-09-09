## KU Polls and Surveys
[![Django CI](https://github.com/Nantawat6510545543/ku-polls/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/Nantawat6510545543/ku-polls/actions/workflows/django.yml)

This is Web application for polls and surveys at Kasetsart University.  
App created as part of
the [Individual Software Process](https://cpske.github.io/ISP) course at
Kasetsart University.

## Install and Run

### Install instructions

1. Clone this repository by using this command on terminal

```
git clone https://github.com/Nantawat6510545543/ku-polls.git
```

2. Change directory to project directory

```
cd ku-polls
```

3. Create a virtual environment

for **Mac/Linux** use this command:

```
python -m venv env           # create the virtual env in "env/", only 1 time
. env/bin/activate           # start the virtual env in bash or zsh
```

for **Windows** use this command:

```
python -m venv env
. .\env\Scripts\activate
```

5. Install dependencies by following command

```
pip install -r requirements.txt
```

6. Create a new database by running migrations

```
python manage.py migrate
```

7. Then import data using “loaddata”

```
python manage.py loaddata data/polls.json data/users.json
```

### How to run

1. To run the server

```
python manage.py runserver
```

2. To access the app at http://localhost:8000

3. To deactivate the virtual environment

```
deactivate
```

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Development Plan](../../wiki/Development-Plan)

### Iterations
- [Iteration 1 Plan](../../wiki/Iteration-1-Plan)
- [Iteration 2 Plan](../../wiki/Iteration-2-Plan)
- [Iteration 3 Plan](../../wiki/Iteration-3-Plan)
- [Iteration 4 Plan](../../wiki/Iteration-4-Plan)
- [Task Board](../../projects)

[django-tutorial]: TODO-write-the-django-tutorial-URL-here
