#!/bin/bash
export postgres_host=postgres/postgres_db
export postgres_user=postgres_user
export postgres_password=postgres_password

poetry run alembic revision --autogenerate -m "migration"
poetry run alembic upgrade head
poetry run gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80    