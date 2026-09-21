#!/bin/sh

set -e

echo "Running initial character set update..."
cd /opt
python -m game_data.app || exit 1
python -m game_data.load_items || exit 1
python -m game_data.load_units || exit 1

echo "Starting cron..."
exec /usr/sbin/crond -f