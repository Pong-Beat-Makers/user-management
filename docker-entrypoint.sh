python manage.py makemigrations social_login
python manage.py migrate social_login

gunicorn -b 0.0.0.0 -p 8000 userManagement.wsgi:application