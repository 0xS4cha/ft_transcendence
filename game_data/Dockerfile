FROM python:3.12.14-alpine3.24

RUN mkdir -p /opt/game_data/
WORKDIR /opt/game_data/

COPY ./src/*.py .
COPY ./crontab .

RUN /usr/bin/crontab /opt/game_data/crontab

RUN pip install --no-cache-dir requests pydantic SQLAlchemy psycopg2-binary

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["/opt/game_data/entrypoint.sh"]