heroku container:login
if [ $CIRCLE_BRANCH = 'master' ]; then heroku git:remote -a programs-registry; fi
if [ $CIRCLE_BRANCH = 'develop' ]; then heroku git:remote -a programs-registry-dev; fi
heroku container:push web
