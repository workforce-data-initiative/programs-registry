FROM brighthive/python
WORKDIR /programs_registry
COPY . /programs_registry

ENV FLASK_APP="programs_registry"
ENV FLASK_ENV="development"
EXPOSE 5000

CMD ./init.sh
