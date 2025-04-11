#!/bin/bash

echo "Applying migrations..."
python -m alembic upgrade head

echo "Starting application..."
exec python main.py