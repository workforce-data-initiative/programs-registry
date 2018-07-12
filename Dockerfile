FROM brighthive/python
LABEL Description="Image for Programs Registry API Flask application"
# for psycopg2 to work
RUN apt-get -y install libcurl4-openssl-dev

WORKDIR /programs_registry
COPY . /programs_registry

ENV FLASK_APP="program_registry"
ENV FLASK_ENV="production"
EXPOSE 5000

CMD ./init.sh  

# TODO: switch to gunicorn for running production server

