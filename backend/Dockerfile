FROM    python:3.14-slim-bookworm AS builder

COPY    --from=ghcr.io/astral-sh/uv:0.12.8 /uv /uvx /bin/

ENV     UV_COMPILE_BYTECODE=1 \
        UV_LINK_MODE=copy

WORKDIR /app

COPY    app/pyproject.toml app/uv.lock ./

RUN     --mount=type=cache,target=/root/.cache/uv \
        uv sync --frozen --no-install-project --no-dev

COPY    app/ .

RUN     --mount=type=cache,target=/root/.cache/uv \
        uv sync --frozen --no-dev



FROM    python:3.14-slim-bookworm

RUN     apt-get update && \
        apt-get install -y --no-install-recommends wget && \
        rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY    --from=builder /app/.venv /app/.venv
COPY    --from=builder /app/src /app/src

ENV     PATH="/app/.venv/bin:$PATH"

CMD     ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"]