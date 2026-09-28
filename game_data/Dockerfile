FROM python:3.12.14-alpine3.24

RUN mkdir -p /opt/game_data/
WORKDIR /opt/game_data/

COPY ./src/*.py .
RUN mkdir -p ./fetch_matches/
COPY ./src/fetch_matches/load_in_db.py ./fetch_matches/
COPY ./src/fetch_matches/__init__.py ./fetch_matches/
COPY ./src/fetch_matches/*.json ./fetch_matches/
COPY ./crontab .
COPY ./src/*.json ./

RUN /usr/bin/crontab /opt/game_data/crontab

RUN pip install --no-cache-dir requests pydantic SQLAlchemy psycopg2-binary httpx2 aiofiles fastapi pydantic_settings asyncpg sqlalchemy[asyncio]

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["/opt/game_data/entrypoint.sh"]