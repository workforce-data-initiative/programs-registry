FROM brighthive/python
ARG HEROKU_DATASTORE_URI
WORKDIR /programs_registry
COPY . /programs_registry

ENV FLASK_APP="programs_registry"
ENV FLASK_ENV="production"
ENV DATABASE_URL=$HEROKU_DATASTORE_URI

CMD ./init.sh
