FROM python:3.6
WORKDIR /app
# For psycopg2 to work
RUN apt-get install libcurl4-openssl-dev
ADD requirements.txt .
RUN pip install -r requirements.txt
ENV APP_SETTINGS="production"
ADD . .
CMD ./init.sh
