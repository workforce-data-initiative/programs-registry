# program-registry
A comprehensive directory of youth programs and services – openly available and machine readable.

# Development Setup
## Steps
### Prerequisites
- Python3
- pip
- Postgres (with a database 'registry' created)

### Run the following commands

If it is your first time, create the database and run migrations by running:
```bash
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```
Then install required python packages and export environment variables by running:

```bash
pip install -r requirements.txt
export FLASK_APP=app.py
export APP_SETTINGS="development"
export DATABASE_URL=postgresql://localhost:5432/registry
python3 app.py
```

The API is now accessible from: `0.0.0.0:5000/api` and the API spec at: `0.0.0.0:5000/api/ui/`

> Endpoints

So the urls are:
`/api` - as the main API endpoint
`/api/ui/` - as the API SPEC url endpoint

# Testing
Run `python3 manage.py test` after following the Development Setup above.


# Docker workflow
## Steps
### Prerequisites
- docker (Download it from [here](https://www.docker.com/get-docker) and choose `Get Docker` for either the desktop version or server version)

### Run the following command

```bash
docker-compose up
```

# Deployment
This project is using `Heroku Container Registry` for automatic deployments of master and develop branches. It is part of the CI/CD pipeline as detailed in [heroku.sh](/heroku.sh).

> Please note

The Postgres Add-on does not have automatic reset for each deployment so the developers will need to reset the DB whenever we have changes to the models.

To do this click on either [this link](https://dashboard.heroku.com/apps/programs-registry-dev/resources) for `develop` branch or [this other link](https://dashboard.heroku.com/apps/programs-registry/resources) for `master` branch; then click on `Heroku Postgres :: Database` which redirects you to the Datastore. Click on `Settings` then select `Reset Database`. Finally get back to the heroku app, click on `More` and select `Restart all dynos`.
