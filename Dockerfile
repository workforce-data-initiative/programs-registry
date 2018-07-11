FROM python:3.6
WORKDIR /app
# For psycopg2 to work
RUN apt-get install libcurl4-openssl-dev
ADD requirements.txt .
RUN pip install -r requirements.txt

# environment variables
# FLASK_APP=program_registry
# DATABASE_URL=postgresql://regdb:@${PGSQL_SERVER_HOSTNAME}:${PGSQL_PORT}/registry
# FLASK_ENV="production"

ENV APP_SETTINGS="production"
ADD . .
CMD ./init.sh
