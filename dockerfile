FROM python:3.9-rc-buster

WORKDIR /opt/url
COPY . .

RUN pip install --no-cache-dir -r ./requirements.txt && \
    chown 1000:1000 -R /opt/url

EXPOSE 9090

ENTRYPOINT [ "uwsgi", "-w", "wsgi:app", "--uid", "1000", "--http", ":9090","--master", "--workers", "3"]