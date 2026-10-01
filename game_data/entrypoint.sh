#!/bin/sh

set -e

echo "Running initial 3d model download..."
cd /opt

python -m game_data.load_3d_models || exit 1

echo "Finished task..."
tail -f /dev/null