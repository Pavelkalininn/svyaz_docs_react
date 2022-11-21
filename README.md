# Enterprise word documents quick filler (in progress). Expected result is a React web and desctop native application.

I am starts the project developing. Have not workflow yet.


## Description

Backend:
    Django rest framework

Frontend:
    React web application
    React Native application

## Technology

    Django==3.2.16
    django-filter==22.1
    django-templated-mail==1.1.1
    djangorestframework==3.13.1
    djangorestframework-simplejwt==4.8.0
    djoser==2.1.0
    PyJWT==2.4.0
    python-dotenv==0.20.0
    requests==2.28.1
    gunicorn==20.1.0
    psycopg2-binary==2.9.3
    pandas==1.3.5
    openpyxl==3.0.10
    redis==4.3.4

## Env file template path: 

[infra/example.env](./infra/example.env)

The DOCKER_USERNAME variable must be present in the Github secrets environment to run CI

## Project run:

### It is necessary to execute the commands in the infra folder to launch a project, apply migrations, create a superuser, load static, respectively:
    
    docker-compose -f docker-compose_prod.yml up -d --build
    docker-compose -f docker-compose_prod.yml exec web python manage.py migrate
    docker-compose -f docker-compose_prod.yml exec web python manage.py loaddata test_fixtures.json
    docker-compose -f docker-compose_prod.yml exec web python manage.py createsuperuser
    docker-compose -f docker-compose_prod.yml exec web python manage.py collectstatic --no-input

You need change docker-compose_prod.yml on docker-compose_develop.yml for running application in development mode with open ports and additional abilities


Author: [__Pavel Kalinin__](https://github.com/Pavelkalininn)
