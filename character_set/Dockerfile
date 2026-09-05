FROM python:3.12.14-alpine3.24

RUN mkdir -p /opt/character_set/
WORKDIR /opt/character_set/

COPY ./*.py .
COPY ./crontab .

RUN /usr/bin/crontab /opt/character_set/crontab

RUN pip install --no-cache-dir \
    requests \
    pydantic \
    SQLAlchemy \
    psycopg2-binary

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

CMD ["/opt/character_set/entrypoint.sh"]