#!/bin/sh
# Run the backend test suite against a throwaway Postgres + Redis.
# Nothing touches the real stack: separate network, containers and a copy of shared/.
#
#   ./backend/app/tests/run_in_docker.sh                 # whole suite
#   ./backend/app/tests/run_in_docker.sh -k chat -x      # any pytest args
#
# Uses the image of the running transcendence-backend container (build it first
# with `make build` if needed).
set -eu

ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
APP="$ROOT/backend/app"
NET=transcendence-test-net
TMP=$(mktemp -d)
IMG=${TEST_IMAGE:-$(docker inspect transcendence-backend -f '{{.Image}}')}

cleanup() {
    docker rm -f transcendence-test-runner transcendence-test-pg transcendence-test-redis >/dev/null 2>&1 || true
    docker network rm "$NET" >/dev/null 2>&1 || true
    rm -rf "$TMP"
}
trap cleanup EXIT INT TERM
cleanup

cp -r "$ROOT/shared/." "$TMP/"
rm -rf "$TMP/profile_pictures" && mkdir -p "$TMP/profile_pictures" "$TMP/models_3d"

docker network create "$NET" >/dev/null
docker run -d --name transcendence-test-pg --network "$NET" --network-alias postgres \
    -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test postgres:15 >/dev/null
docker run -d --name transcendence-test-redis --network "$NET" --network-alias redis redis:7-alpine >/dev/null

docker run -d --name transcendence-test-runner --network "$NET" --entrypoint sleep \
    -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test \
    -e SECRET_JWT_KEY=test-secret-key-0123456789abcdef0123456789abcdef -e RIOT_API_KEY=dummy \
    -e FORTYTWO_CLIENT_ID=cid -e FORTYTWO_CLIENT_SECRET=csecret \
    -e FORTYTWO_REDIRECT_URI=https://localhost:8443/api/auth/login_with_42/callback \
    -e HOST_IP=127.0.0.1 -e CONTAINER_NAME=backend -e DEBUG=0 \
    -v "$APP/src:/app/src" -v "$TMP:/app/src/shared" -v "$APP/tests:/app/tests" \
    -v "$APP/alembic:/app/alembic" -v "$APP/alembic.ini:/app/alembic.ini" \
    -v "$APP/pyproject.toml:/app/pyproject.toml" -v "$APP/uv.lock:/app/uv.lock" \
    "$IMG" infinity >/dev/null

docker exec -w /app transcendence-test-runner sh -c '
    # sync first: the image venv points at an interpreter missing from the image (audit H10)
    uv sync --frozen --inexact -q
    until .venv/bin/python -c "import socket; socket.create_connection((\"postgres\", 5432), 1)" 2>/dev/null; do sleep 1; done
    sleep 2
    uv run --frozen alembic upgrade head >/dev/null
'
docker exec -w /app transcendence-test-runner .venv/bin/pytest -p no:cacheprovider "$@"
