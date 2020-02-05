release: python manage.py migrate; python manage.py loaddata core/fixtures/data_prueba.json; pip install python-pdf
web: gunicorn pycronos.wsgi