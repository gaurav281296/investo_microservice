set -e
python manage.py makemigrations basket
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn investo.wsgi -w 3 -t 45 -b "0.0.0.0:8000"