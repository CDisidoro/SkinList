#!/bin/bash

while !</dev/tcp/db/3306; do sleep 1; done;
port=$(printenv PORT)
python manage.py makemigrations wishlist
python manage.py sqlmigrate wishlist 0001
python manage.py migrate
rm wishlist/migrations/0001_initial.py
cron
python manage.py update_cosmetics
python manage.py fetch_shop
python manage.py runserver 0.0.0.0:$port
#python manage.py runsslserver 0.0.0.0:$port --certificate /app/cert/cert.pem --key /app/cert/key.pem