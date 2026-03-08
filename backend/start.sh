#!/bin/bash
# Railway startup script

# Use Railway's PORT or default to 5000
export PORT=${PORT:-5000}

echo "Starting application on port $PORT"

# Run gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 "app:create_app()"
