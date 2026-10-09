FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.8 /uv /uvx /bin/

# Use the image's Python 3.14: a uv-downloaded interpreter would not be copied
# to the final stage and the venv would point at nothing.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY app/pyproject.toml app/uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY app/ .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.14-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /bin/uv /bin/uvx /bin/

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/alembic /app/alembic
COPY --from=builder /app/alembic.ini /app/alembic.ini
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src \
    UV_PYTHON_DOWNLOADS=never

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "3000", "--proxy-headers", "--forwarded-allow-ips=172.18.0.0/16"]
