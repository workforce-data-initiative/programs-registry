FROM brighthive/python

# for psycopg2 to work
RUN apt-get update && apt-get -y install python-dev libpq-dev

WORKDIR /programs_registry
COPY . /programs_registry

ENV FLASK_APP="programs_registry"
ENV FLASK_ENV="development"
EXPOSE 5000

RUN pip install -r requirements.txt
CMD ./init.sh