FROM python:3.6
ARG HEROKU_DATASTORE_URI
WORKDIR /app
# For psycopg2 to work
RUN apt-get install libcurl4-openssl-dev
ADD requirements.txt .
RUN pip install -r requirements.txt
ENV APP_SETTINGS="production"
ENV DATABASE_URL=$HEROKU_DATASTORE_URI
ENV FLASK_APP=app.py
ADD . .
CMD ./init.sh
