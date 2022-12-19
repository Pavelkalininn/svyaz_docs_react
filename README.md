# Enterprise word documents quick filler (in progress). Expected result is a React web and desktop native application.

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
    djangorestframework==3.14.0
    djoser==2.1.0
    flake8==5.0.4
    isort==5.10.1
    psycopg2-binary==2.9.5
    python-dotenv==0.21.0
    gunicorn==20.1.0
    celery==5.2.7
    python-docx==0.8.11
    redis==4.4.0

## Env file template path: 

[infra/example.env](./infra/example.env)

The DOCKER_USERNAME variable must be present in the Github secrets environment to run CI

## Project run:

### It is necessary to execute the commands in the infra folder to launch a project, apply migrations, create a superuser, load static, respectively:
    
    docker-compose -f docker-compose_develop.yml up -d --build
    docker-compose -f docker-compose_develop.yml exec backend python manage.py migrate
    docker-compose -f docker-compose_develop.yml exec backend python manage.py loaddata db.json
    docker-compose -f docker-compose_develop.yml exec backend python manage.py createsuperuser
    docker-compose -f docker-compose_develop.yml exec backend python manage.py collectstatic --no-input

You need change docker-compose_prod.yml on docker-compose_develop.yml for running application in development mode with open ports and additional abilities


Author: [__Pavel Kalinin__](https://github.com/Pavelkalininn)
