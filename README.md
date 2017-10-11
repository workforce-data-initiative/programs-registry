# chi-program-registry
A comprehensive directory of youth programs in Chicago – openly available and machine readable.

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
