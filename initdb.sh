#!/bin/bash
source ../.pve/bin/activate
rm db.sqlite3
rm -r /backend/migrations/*
python3 manage.py makemigrations backend
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
