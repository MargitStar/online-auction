FROM python:3.9

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.6

WORKDIR /code
COPY pyproject.toml poetry.lock /code/

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry install

COPY . /code/