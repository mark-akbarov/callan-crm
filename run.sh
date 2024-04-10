#!/bin/bash

cd /home/mrk/callan-crm
source .venv/bin/activate
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
