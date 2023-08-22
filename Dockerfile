# Pull base image
FROM python:3.10-slim as base

WORKDIR /code

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get upgrade -y -q
# RUN apt-get install -y -q git

# Configuring poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

#Copying to code
COPY poetry.lock /code
COPY pyproject.toml /code
COPY system code/

RUN poetry install --only main

FROM base as debug

RUN poetry install --only debugpy

CMD ["sh", "-c", "python -m debugpy --wait-for-client --listen 0.0.0.0:5678 -m system"]

FROM base as local

CMD ["sh", "-c", "python -m system"]

FROM base as test

RUN poetry install --only dev
CMD ["sh", "-c", "coverage run -m unittest -v;coverage report;exit 0"]
