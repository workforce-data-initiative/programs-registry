# program-registry
A comprehensive directory of youth programs and services – openly available and machine readable.

# Design and Documentation
The API spec can be publicly viewed [here](https://app.swaggerhub.com/apis/BrightHive/program-registry) and is hosted [here](https://docs.brighthive.io/v1.0/reference#organization).

The folder [.openapi](/openapi) was generated automatically by SwaggerHub. We have set up [`Github Sync`](https://app.swaggerhub.com/help/integrations/github-sync) for the API spec on Swaggerhub. It promises to automatically update the spec on Github with changes done in SwaggerrHub. The API design and documentation process, therefore, is that all stakeholders collaborate on SwaggerHub and the update is synced on Github upon save.

> NB

We noted however that this integration is still buggy (It doesn't sync with Github on save). The integration works well for setting up this workflow for a new repo. So we activated [`Github Push`](https://app.swaggerhub.com/help/integrations/github-push) for the syncing. The spec file is at [.openapi/swagger.yaml](.openapi/swagger.yaml).

### To adopt this workflow

For a similar workflow, you'll find that the docs in [`Github Push`](https://app.swaggerhub.com/help/integrations/github-push) and [`Github Sync`](https://app.swaggerhub.com/help/integrations/github-sync) are quite straight forward.

Be sure to set:
- a separate branch other that the main ones (In our case we chose *SWAGGERHUB*)
- swagger output folder as `.openapi` and 
- swagger file as `swagger.yaml`

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
