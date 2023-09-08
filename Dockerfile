FROM python:3.11

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN apt-get update && \
    apt-get install -y openssl

COPY generate-certificate.sh /tmp/generate-certificate.sh

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - && \
    cd /usr/local/bin && \
    ln -s /etc/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN bash -c "poetry install --no-root --no-dev"

COPY . /app

RUN chmod +x /tmp/generate-certificate.sh

RUN bash -c "/tmp/generate-certificate.sh"

CMD [ "python", "app/main.py" ]
