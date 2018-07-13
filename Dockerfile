FROM brighthive/python
LABEL Description="Image for Programs Registry API Flask application"
WORKDIR /programs_registry
COPY . /programs_registry

ENV FLASK_APP="programs_registry"
ENV FLASK_ENV="production"
EXPOSE 5000

CMD ./init.sh

# TODO: switch to gunicorn for running production server
