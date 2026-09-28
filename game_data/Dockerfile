FROM python:3.12.14-alpine3.24

RUN mkdir -p /opt/game_data/
WORKDIR /opt/game_data/

COPY ./src/*.py .
COPY ./src/*.json ./

RUN pip install --no-cache-dir requests pydantic SQLAlchemy psycopg2-binary httpx2 aiofiles fastapi pydantic_settings asyncpg greenlet sqlalchemy[asyncio]

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["/opt/game_data/entrypoint.sh"]