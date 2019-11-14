release: python manage.py migrate; python manage.py loaddata core/fixtures/*.json
web: gunicorn pycronos.wsgi