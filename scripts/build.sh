#!/bin/bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml exec web python manage.py makemigrations
docker-compose -f docker-compose.yml exec web python manage.py migrate
docker-compose -f docker-compose.yml exec web python manage.py collectstatic --noinput
docker-compose -f docker-compose.yml exec web python manage.py createsuperuser
docker-compose -f docker-compose.yml exec web python manage.py runserver 0.0.0.0:8000