#!/bin/sh

set -e

echo "Alembic upgrade start..."
alembic upgrade head

echo "FastAPI Startup..."
# The command comes from the image CMD (prod: fastapi run) or compose.dev.yaml (dev: fastapi dev).
exec "$@"
