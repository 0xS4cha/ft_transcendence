#!/bin/sh

set -e

echo "Alembic upgrade start..."
uv run alembic upgrade head

echo "FastAPI Statup..."
exec fastapi dev --host 0.0.0.0 --port 3000 --proxy-headers --forwarded-allow-ips="172.18.0.0/16"