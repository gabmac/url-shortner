# Pull base image
FROM python:3.10-slim

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

# Exports poetry dependencies to a requirements.txt file
ARG INSTALL_COMMAND
RUN $INSTALL_COMMAND
