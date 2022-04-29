#!/usr/bin/env bash

echo "Waiting for database..."
while ! nc -z ${DB_HOST} ${DB_PORT}; do sleep 2; done
echo "Connected to database."

echo "Controling database user status..."
PSQL_CONNECTION="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
while ! psql $PSQL_CONNECTION -c select 1; do sleep 5; done
echo "Database user exists."

if [[ "$ENV" = "DEVELOPMENT" ]]
then
  python manage.py migrate --noinput
  if [ $? -ne 0 ]; then
      echo "Migration failed." >&2
      exit 1
  fi

  python manage.py collectstatic --noinput
fi

echo "Starting Gunicorn..."
exec gunicorn AIC22_Backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers $GUNICORN_WORKER_NUMBER \
    --log-level=info \
    --log-file=- \
    --access-logfile=- \
    --error-logfile=- \
    --timeout 90 \
    --reload