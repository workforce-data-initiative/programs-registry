docker login --username=_ --password=$(heroku auth:token) registry.heroku.com
if [ $CIRCLE_BRANCH = 'master' ]; then heroku git:remote -a programs-registry; fi
if [ $CIRCLE_BRANCH = 'develop' ]; then heroku git:remote -a programs-registry-dev; fi
heroku container:push web
