#!/bin/bash -xe

# Allows to see errors as they occur
exec 2>&1

sleep 5

pip install -e .

if [ ! -d "./migrations" ]; then
  # Control will enter here if migrations directory doesn't exist
  flask db init
  flask db migrate
fi

flask db upgrade schema
flask test --all

flask run

