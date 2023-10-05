FROM python:3.10

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        netcat-traditional \
        python3-dev \
        dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./docker/server/entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/entrypoint.sh

RUN dos2unix /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/usr/local/bin/entrypoint.sh"]
