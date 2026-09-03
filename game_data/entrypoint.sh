#!/bin/sh

set -e

echo "Running initial character set update..."
cd /opt
python -m game_data.app

echo "Starting cron..."
exec /usr/sbin/crond -f