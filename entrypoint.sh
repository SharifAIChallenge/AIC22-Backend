#!/bin/bash
python manage.py migrate sites
python manage.py migrate
python manage.py crontab add
gunicorn --bind=0.0.0.0:8000 --timeout=90 --preload AIC22_Backend.wsgi:application

