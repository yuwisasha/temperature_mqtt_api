FROM python:3.11

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - && \
    cd /usr/local/bin && \
    ln -s /etc/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN bash -c "poetry install --no-root --no-dev"

COPY . /app

RUN python /app/main.py