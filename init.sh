#!/bin/bash -xe

# Allows to see errors as they occur
exec 2>&1

sleep 5

if [ ! -d "./migrations" ]; then
  # Control will enter here if migrations directory doesn't exist
  pipenv run flask db init
  pipenv run flask db migrate
fi

pipenv run flask db upgrade schema
pipenv run flask test --all

pipenv run flask run
