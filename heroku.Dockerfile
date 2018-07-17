FROM brighthive/python
ARG HEROKU_DATASTORE_URI

# for psycopg2 to work
RUN apt-get update && apt-get -y install python-dev libpq-dev

WORKDIR /programs_registry
COPY . /programs_registry

ENV FLASK_APP="programs_registry"
ENV FLASK_ENV="production"
ENV DATABASE_URL=$HEROKU_DATASTORE_URI

RUN pip install -e .
CMD ./init.sh
