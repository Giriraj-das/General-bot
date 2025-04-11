#!/bin/sh

echo "Applying migrations..."
python -m alembic upgrade head

if [ $? -ne 0 ]; then
    echo "Migration failed!"
    exit 1
fi

echo "Starting application..."
exec python main.py