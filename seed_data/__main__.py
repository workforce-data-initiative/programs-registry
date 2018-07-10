# -*- coding: utf-8 -*-

import os
import sys
import re
import logging
from psycopg2 import IntegrityError, DataError
from sqlalchemy import create_engine


# set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('seed_data')

def load_csv(connection, tables):
    """Load db tables from CSV files
    
    NOTE: First row in each file is expected
    to be the header row
    
    """
    
    log.info('Load from CSV input file')
    csv_path = os.path.join(os.path.dirname(__file__), 'csv')
    cursor = connection.cursor()
    
    try:
        for table in tables:
            csv_data = os.path.join(csv_path, '{}.csv'.format(table))
            log.info('Loading {} table data from {}'.format(table, csv_data))
    
            with open(csv_data, 'r') as csv_file:
                next(csv_file, None)            
                cursor.copy_from(csv_file, table, sep='|', null='NULL')
    except (DataError, IntegrityError) as err:
            connection.rollback()
            err_msg = 'Loading table {} from CSV file - {}Rolled back all'.format(table,err)
            log.error(err_msg, exc_info=False)
            raise
    else:
        log.info('Committing all')
        connection.commit()

def load_sql(connection, tables):
    """Load db table from SQL file
    
    NOTE: Does not handle SQL statements 
    spanning multiple lines
    
    """
    
    log.info('Load using SQL INSERT, this may take more time')
    sql_path = os.path.join(os.path.dirname(__file__), 'sql')
    cursor = connection.cursor()
    
    try:
        for table in tables:
            sql_data = os.path.join(sql_path, '{}.sql'.format(table))
            log.info('Loading {} table data from {}'.format(table, sql_data))
        
            with open(sql_data, 'r') as sql_file:
                for line in sql_file:  
                    log.info(line)
                    cursor.execute(line)
    except (DataError, IntegrityError) as err:
        connection.rollback()
        err_msg = 'SQL INSERT on {} table - {}Rolled back all'.format(table, err)
        log.error(err_msg, exc_info=False)
    else:
        log.info('Committing all')
        connection.commit()

def create_conn(database_url):
    """Create raw psycopg connection to database and
    get cursor on this this connection
    
    @param database_url: in the format 
                        postgresql://regdb:@${PGSQL_SERVER_HOSTNAME}:${PGSQL_PORT}/registry
    @return: cursor on db connection
    """
     
    psycopg_url = re.sub('^postgresql', 'postgresql+psycopg2', database_url)
    engine = create_engine(psycopg_url)
    return engine.raw_connection()


conn = create_conn(os.environ.get('DATABASE_URL'))
tables = ['entity_type', 'format', 
          'potential_outcome', 'prerequisite',
          'organization', 'location', 
          'physical_address', 'program', 
          'service', 'service_location']

try:
    load_csv(conn, tables)
except Exception as err:
    log.warn(err, exc_info=False)
    load_sql(conn, tables)

log.info('Data load successful for tables {}'.format(tables))
