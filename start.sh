#!/bin/bash
set -e
python manage.py migrate
gunicorn mysite.wsgi:application --bind 0.0.0.0:8000