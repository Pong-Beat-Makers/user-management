set -e
python manage.py makemigrations
python manage.py migrate

gunicorn -b 0.0.0.0 -p 8000 userManagement.wsgi:application
