#!/bin/bash
set -e
python manage.py migrate
gunicorn mysite.wsgi:application
