web: DJANGO_SETTINGS_MODULE=mysite.settings.production gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
release: DJANGO_SETTINGS_MODULE=mysite.settings.production python manage.py migrate && python manage.py collectstatic --noinput
