FROM brighthive/python
LABEL Description="Image for Programs Registry API Flask application"

# for psycopg2 to work
RUN apt-get update && apt-get -y install python-dev libpq-dev

WORKDIR /programs_registry
COPY . /programs_registry

ENV FLASK_APP="programs_registry"
ENV FLASK_ENV="production"
EXPOSE 5000

RUN pip install -e .
CMD ./init.sh  

# TODO: switch to gunicorn for running production server

