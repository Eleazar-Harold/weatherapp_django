#!/usr/bin/env bash
set -e
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('eleazar', 'eleazar.yewa.harold@gmail.com', 'Pass@word!#')" | python manage.py shell
# rm -rf static 
# echo yes | python manage.py collectstatic
exec gunicorn --bind=0.0.0.0:80 main.wsgi --workers=5 --log-level=info --log-file=---access-logfile=- --error-logfile=- --timeout 30000 --reload