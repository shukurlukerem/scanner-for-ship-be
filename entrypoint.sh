#!/bin/bash
set -e

echo "🔧 Loading environment variables..."

# Env dəyişkənlərini yoxlayır
: "${POSTGRES_HOST:?POSTGRES_HOST not set}"
: "${POSTGRES_PORT:?POSTGRES_PORT not set}"
: "${POSTGRES_DB:?POSTGRES_DB not set}"
: "${POSTGRES_USER:?POSTGRES_USER not set}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD not set}"

echo "🕓 Waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT}..."

# Postgres hazır olana qədər gözləyir
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "⏳ PostgreSQL is unavailable - waiting..."
  sleep 1
done

echo "✅ PostgreSQL is up - continuing..."

# Migrations
echo "🔄 Running migrations..."
python manage.py migrate --noinput

# Static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Gunicorn başlat
echo "🚀 Starting Gunicorn..."
exec gunicorn ship_scanner.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 2 \
    --timeout 120

