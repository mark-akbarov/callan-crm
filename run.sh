#!/bin/bash

cd /home/mrk/callan-crm
source .venv/bin/activate
<<<<<<< HEAD
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
=======
exec python manage.py runserver 0.0.0.0:8000
# exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
>>>>>>> 2212e8b (minor fix)
