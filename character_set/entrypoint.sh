#!/bin/sh

set -e

find /opt/character_set -maxdepth 3 -type f -print

echo "Running initial character set update..."
cd /opt
python -m character_set.app

echo "Starting cron..."
exec /usr/sbin/crond -f