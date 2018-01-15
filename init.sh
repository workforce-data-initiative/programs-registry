#!/bin/bash -xe

# Allows to see errors as they occur
exec 2>&1

sleep 5

DIRECTORY=migrations
if [ ! -d "$DIRECTORY" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  python3 manage.py db init
fi
python3 manage.py db migrate
python3 manage.py db upgrade
python3 manage.py test
python3 app.py
