#!/bin/bash
python manage.py makemigrations &&
python manage.py migrate &&
python manage.py collectstatic --noinput &&
gunicorn CalFoscari.wsgi:application --bind 0.0.0.0:8003