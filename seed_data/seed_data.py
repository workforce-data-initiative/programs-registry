import logging
import os
import sys
from urllib.parse import urlparse

import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

result = urlparse(os.getenv('DATABASE_URL'))
# In the format: "postgresql://postgres:postgres@localhost:5432/postgres"
# or: "postgresql://localhost:5432/postgres"
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

logger.info('Connecting to database')
connection = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname
)
logger.info('Database connected')
logger.debug('Database {} is on host {}'.format(database, hostname))

tables = ['organization', 'location', 'physical_address', 'program', 'service',
          'service_location']

for table in tables:
    cur = connection.cursor()
    try:
        with open('data/' + table + '.csv', 'r') as f:
            if sys.argv[-1] != 'no_header':
                next(f)  # Skip the header row.
            cur.copy_from(f, table, sep=',')

    except psycopg2.DataError as error:
        logger.info('Bumped into an error {}'.format(error))
        logger.info('Trying something else')
        with open('data/' + table + '.sql', 'r') as f:
            if sys.argv[-1] != 'no_header':
                for line in f[1:]:  # Skip the header row.
                    cur.execute(line)
            else:
                for line in f:
                    cur.execute(line)

    connection.commit()
    logger.info('Entries for {} successful'.format(table))
