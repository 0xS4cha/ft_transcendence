FROM        python:3.14-slim-bookworm AS builder

RUN         pip install --upgrade pip setuptools wheel

WORKDIR     /app

RUN         python -m venv .venv
ENV         PATH="/app/.venv/bin:$PATH"

COPY        requirements.txt .

RUN         --mount=type=cache,target=/root/.cache/pip \
            pip install -r requirements.txt

COPY        . .


FROM        python:3.14-slim-bookworm AS runtime

ENV         PATH="/app/.venv/bin:$PATH"

WORKDIR     /app

COPY        --from=builder /app .

ENTRYPOINT  ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]