#!/bin/bash

echo "Applying database migrations..."
alembic upgrade head

echo "Seeding database..."
cd src
python -m database.seed_db

echo "Starting Gunicorn..."
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000