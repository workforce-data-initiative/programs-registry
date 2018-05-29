# Training Provider Outcomes Toolkit - Programs Registry API
Machine readable, public directory of programs and services offered by eligible training providers across locations. See the [BrightHive API Documentation](https://docs.brighthive.io) for the full Programs Registry API specification.


## Developer Guide

How to setup in your local development environment

### Prerequisites

1. Have Python v3.6+ available, including package manager `pip` 
2. Have a virtual environment manager for Python available e.g `virtualenv`
	
	```bash
	python3 -m pip install -U virtualenv	
	```

3. Create and/or connect to a Postgres v9.6+ database instance (a public docker image is a decent option)

### Setup Environment

1. Login to the Postgres database instance as a privileged user and create programs registry database. From command line:

	```bash
	useradd --user-group regdb 
	su - ${PG_DEFAULT_ADMIN}  # generally default admin user is 'postgres'
	psql --command "CREATE USER regdb; ALTER USER regdb SUPERUSER CREATEDB;" 
	createdb --echo --owner=regdb --encoding=utf-8 registry
	```

**_Note: If there's need to drop existing database to resolve issues_**

	```bash
	dropdb --echo regdb
	```

2. Get the code to your local environment

	```bash
	git clone ${GITHUB_CLONE_URL}
	cd program_registry
	```

3. Create and activate a python virtual environment using Python 3.6+ interpreter

	```bash
	python3 -m venv ${VENV_NAME} ${ENV_DIR}
	. ${ENV_DIR}/${VENV_NAME}/bin/activate
	```

4. Set required environment variables for running Flask application

	```bash
	export FLASK_APP=program_registry
	export FLASK_ENV="development"
	export DATABASE_URL=postgresql://regdb:@${PGSQL_SERVER_HOSTNAME}:${PGSQL_PORT}/registry
	```

5. Pip install Flask application all it's dependencies

	```bash 
	pip install -e .
	```
	
6. Load program registry database

	* Option 1(Recommended): Create and seed tables using migration script
	
	```bash
	flask db upgrade seed
	```

	* Option 2 (Maybe faster in some instances): Create and seed tables using CSV or SQL file data

	```bash
	flask db upgrade schema
	python -m seed_data 
	```
	
	* To drop seed data from the database
	
	```bash
	flask db downgrade
	```
	
	Note: In the case of Option 2, this will drop all tables as well because the data load happens outside migrations.

7. Run tests, with any of the following options
	
	```bash
	flask test --all
	flask test endpoints
	flask test endpoints,models
	```
	
### Run Development Server

1. Start Flask app server

	```bash
	flask run --host ${FLASK_RUN_HOST} --port ${FLASK_RUN_PORT}
	```

2. API can then be accessed from base url `https://${FLASK_RUN_HOST}:${FLASK_RUN_PORT}/api/v1`


### Access API Documentation

The official API documentation is published at [https://docs.brighthive.io](https://docs.brighthive.io) however OpenAPI specification can be made locally available using [Connexion](https://github.com/zalando/connexion#why-connexion) 

```
connexion run -v --host ${FLASK_RUN_HOST} --port ${OPENAPI_SPEC_RUN_PORT} .openapi/openapi.yml
```

Then access the OpenAPI specification using url: `http://${FLASK_RUN_HOST}:${OPENAPI_SPEC_RUN_PORT}/api/v1/ui/`

For any issues with the official API documentation, please [open a documentation issue](https://github.com/brighthive/program-registry/issues).

### Alternative Deployment Options

#### Docker Container

##### Prerequisites

1. Docker install ([Get Docker](https://www.docker.com/get-docker) for your environment) 

##### Create Docker Image

```bash
docker-compose up
```

### Continuous Delivery

As part of CircleCI CI/CD pipeline, this repository uses `Heroku Container Registry` for automatic deployment of master and develop branches to Heroku. See [heroku.sh](https://github.com/brighthive/program-registry/blob/master/heroku.sh) for configurations, these can be updated to run with Heroku app of choice.

**Note**:
The Postgres Add-on does not have automatic reset for each deployment so the developers need to reset the deployed db on Heroku whenever we have changes to the models.

To do this, go to Heroku app resources page (for each branch) > `Heroku Postgres :: Database` which redirects you to the Datastore. Click on `Settings` > `Reset Database`. Finally get back to the Heroku app, click on `More` > `Restart all dynos`.
