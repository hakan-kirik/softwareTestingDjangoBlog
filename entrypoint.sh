#!/bin/bash

pyhton3 ./manage.py makemigrations
python3 ./manage.py migrate

python3 manage.py loaddata ./initial_data.json

python3 ./manage.py runserver 0.0.0.0:3000
