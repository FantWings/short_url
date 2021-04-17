FROM python:3.9-rc-buster

WORKDIR /opt/url
COPY . .

RUN apt-get update && apt-get install -y libmysqlclient-dev

RUN pip install --no-cache-dir -r ./requirements.txt && \
    chown 1000:1000 -R /opt/url

ENV SQL_MODE "sqlite" \
    SQL_USER "" \
    SQL_PASS "" \
    SQL_HOST "" \
    SQL_PORT "" \
    SQL_BASE "" 

EXPOSE 9090

ENTRYPOINT [ "uwsgi", "-w", "wsgi:app", "--uid", "1000", "--http", ":9090" ]