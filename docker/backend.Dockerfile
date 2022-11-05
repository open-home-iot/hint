# syntax=docker/dockerfile:1
# NB!
# LEAVE LABELLING TO THE RELEASE WORKFLOW!

FROM docker.io/python:3.10.8-slim-buster

RUN apt-get update && apt-get install gcc libffi-dev libpq-dev -y && apt-get clean

WORKDIR /app

# Copy needed files
COPY requirements.txt requirements.txt
COPY scripts/migrate-and-run migrate-and-run
COPY manage.py manage.py
COPY backend ./backend

# Update Angular filenames
COPY scripts/replace_angular_file_names.py replace_angular_file_names.py
RUN pip3 install beautifulsoup4
RUN python replace_angular_file_names.py backend/static/collectedstatic/ang backend/templates/index.html
RUN mv backend/templates/built_index.html backend/templates/index.html
RUN pip3 uninstall -y beautifulsoup4
RUN echo "from .base import *\nDEBUG = False" > backend/settings/local.py

# Remove files that aren't needed anymore and that will just serve to bloat
# the image.
RUN rm replace_angular_file_names.py
RUN rm -rf backend/static/*

RUN pip3 install -r requirements.txt

CMD ["./migrate-and-run"]
