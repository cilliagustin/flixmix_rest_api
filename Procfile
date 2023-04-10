release: python manage.py makemigrations && python manage.py migrate
web: gunicorn flixmix_rest_api.wsgi