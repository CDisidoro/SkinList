#!/bin/bash

while !</dev/tcp/db/3306; do sleep 1; done;
port=$(printenv PORT)
python manage.py makemigrations wishlist
python manage.py sqlmigrate wishlist 0001
python manage.py migrate
rm wishlist/migrations/0001_initial.py
python manage.py update_cosmetics
python manage.py fetch_shop
#python manage.py runsslserver
python manage.py runserver 0.0.0.0:$port