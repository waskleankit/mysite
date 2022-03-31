#web: waitress-serve --port=$PORT khargoneblogs.wsgi:application
#web gunicorn khargoneblogs.wsgi:application --log-file -
web: gunicorn khargoneblogs.wsgi --log-file -