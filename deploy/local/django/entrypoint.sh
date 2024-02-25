#!/bin/bash
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate &
gunicorn --preload config.wsgi:application --config=deploy/local/django/gunicorn_conf.py
