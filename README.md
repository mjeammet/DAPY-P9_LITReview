![logo-litreview](https://user.oc-static.com/upload/2020/09/18/16004297044411_P7.png "LITReview logo")

# LITReview

## 1 - Introduction

Django app to ask and post book and articles reviews. 

Marie Jeammet - 2021/10

Programming languages : Python 3.
Framework: Django 3.
Database: SQLite3 

## 2 - Installation

- Clone the repository 
`git clone https://github.com/mjeammet/OCP9_LITReview.git`

- Install the virtual environment, install required packages 
```python -m venv env```
```source env/bin/activate```
```pip install -r requirements.txt```

## 3 - Usage

From the root repo
`source env/bin/activate`
`python manage.py runserver`

to start the development server at [http://127.0.0.1:8000](http://127.0.0.1:8000)

Database has been populated with a few examples, users, tickets and reviews and subscriptions. 

To log in with an pre-generated user:
username: juno
password: -

## 4 - flake8

This repo contains a folder dedicated to flake8 report. The index file shows no flake8 violations.

To generate a new report
- remove existing flake8_report
- edit setup.cfg if you wish to add/remove any folder
- from the root folder, execute
```flake8 --format=html --htmldir=flake8_report```