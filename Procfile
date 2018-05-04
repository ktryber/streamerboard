web: gunicorn config.wsgi:application
worker: celery worker --app=streamerboard.taskapp --loglevel=info
