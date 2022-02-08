python manage.py makemigrations assets linux mysql rds windows system &&
python manage.py migrate &&
#python manage.py runserver 0.0.0.0:8000 > logs/django-web.log 2>&1 &
python manage.py runserver 0.0.0.0:8888
