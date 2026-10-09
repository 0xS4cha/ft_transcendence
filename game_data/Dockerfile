FROM python:3.12.14-alpine3.24

RUN mkdir -p /opt/game_data/
WORKDIR /opt/game_data/

COPY ./src/*.py .
COPY ./src/*.json ./

RUN pip install --no-cache-dir requests==2.34.2 pydantic==2.14.0 "SQLAlchemy[asyncio]==2.1.4" psycopg2-binary==2.9.13 httpx2==2.13.1 aiofiles==25.1.0 fastapi==0.143.0 pydantic-settings==2.15.0 asyncpg==0.32.0 greenlet==3.5.6

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["/opt/game_data/entrypoint.sh"]