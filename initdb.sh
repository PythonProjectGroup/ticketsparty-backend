#!/bin/bash
rm db.sqlite3
rm -r backend/migrations/*
python manage.py makemigrations backend
python manage.py migrate
python manage.py loaddata initial_data.json
python manage.py runserver
