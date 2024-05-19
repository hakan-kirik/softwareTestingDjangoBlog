#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


pyhton3 ./manage.py makemigrations
python3 ./manage.py migrate

python3 manage.py loaddata ./initial_data.json

python3 ./manage.py runserver 0.0.0.0:3000
