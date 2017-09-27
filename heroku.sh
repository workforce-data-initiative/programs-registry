heroku container:login
if [ $CIRCLE_BRANCH = 'master' ]; then heroku git:remote -a chi-pr; fi
if [ $CIRCLE_BRANCH = 'develop' ]; then heroku git:remote -a chi-pr-staging; fi
heroku container:push web
