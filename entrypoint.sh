#!/bin/sh
# Exit immediately if a command exits with a non-zero status
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting the application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload