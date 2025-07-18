web: mkdir -p /app/static_collected && python manage.py collectstatic --noinput && ls -la /app/static_collected && gunicorn bitworks.wsgi:application --bind 0.0.0.0:$PORT
