docker login --username=_ --password=$(heroku auth:token) registry.heroku.com
if [ $CIRCLE_BRANCH = 'master' ]; then export APP=programs-registry; fi
if [ $CIRCLE_BRANCH = 'develop' ]; then export APP=programs-registry-dev; fi

docker build -t registry.heroku.com/$APP/web -f heroku.Dockerfile --build-arg HEROKU_DATASTORE_URI=$HEROKU_DATASTORE_URI .
docker push registry.heroku.com/$APP/web
