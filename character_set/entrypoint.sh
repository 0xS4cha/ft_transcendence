#!/bin/sh

set -e

echo "Running initial character set update..."
python3 /opt/character_set/app.py

echo "Starting cron..."
exec /usr/sbin/crond -f