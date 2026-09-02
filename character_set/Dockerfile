FROM python:3.12.14-alpine3.24

RUN mkdir -p /opt/character_set/
WORKDIR /opt/character_set/

COPY ./*.py .
COPY ./crontab .

RUN /usr/bin/crontab /opt/character_set/crontab

RUN pip install requests pydantic SQLAlchemy psycopg2

RUN python3 /opt/character_set/app.py

CMD ["/usr/sbin/crond", "-f"]