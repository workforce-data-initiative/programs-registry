#!/bin/bash -xe

# Allows to see errors as they occur
exec 2>&1

sleep 5

if [ ! -d "./migrations" ]; then
  # Control will enter here if migrations directory doesn't exist
  flask db init
  flask db migrate
fi

flask db upgrade schema

# TODO: refactor failing tests using seed data
# flask test --all 

flask run