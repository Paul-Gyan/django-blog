#!/bin/bash

python manage.py migrate gunicorn mysite.wsgi:application 