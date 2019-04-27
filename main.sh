#!/usr/bin/env bash
python manage.py makemigrations && 
python manage.py migrate --noinput && 
echo "from django.contrib.auth.models import User; User.objects.create_superuser('eleazar', 'eleazar.yewa.harold@gmail.com', 'Pass@word!#')" | python manage.py shell && 
python manage.py runserver 0.0.0.0:3456