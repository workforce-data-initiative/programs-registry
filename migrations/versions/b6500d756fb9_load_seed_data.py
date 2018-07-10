"""Load db with seed data

Revision ID: b6500d756fb9
Revises: 2faa8fddaa9f
Create Date: 2018-05-17 18:31:35.575053

"""

import os
from alembic import op
from flask import current_app

from common.utils import load_json


# revision identifiers, used by Alembic.
revision = 'b6500d756fb9'
down_revision = '2faa8fddaa9f'
branch_labels = ('seed',)
depends_on = None

target_metadata = current_app.extensions['migrate'].db.metadata
tables = target_metadata.tables
seed_data = os.path.join(os.path.dirname(__file__), '../../', 'seed_data', 'json')

def upgrade(): 
    op.bulk_insert(tables.get('entity_type'),
                   load_json(os.path.join(seed_data, 'entity_type.json')),
                   multiinsert=False)
    op.bulk_insert(tables.get('format'),
                   load_json(os.path.join(seed_data, 'format.json')),
                   multiinsert=False)
    op.bulk_insert(tables.get('potential_outcome'),
                   load_json(os.path.join(seed_data, 'potential_outcome.json')),
                   multiinsert=False)
    op.bulk_insert(tables.get('prerequisite'),
                   load_json(os.path.join(seed_data, 'prerequisite.json')),
                   multiinsert=False)
    op.bulk_insert(tables.get('organization'),
                   load_json(os.path.join(seed_data, 'organization.json')),
                   multiinsert=False)
    op.bulk_insert(tables.get('location'),
                   load_json(os.path.join(seed_data, 'location.json')),
                   multiinsert=False)
    op.bulk_insert(tables.get('program'),
                   load_json(os.path.join(seed_data, 'program.json')),
                   multiinsert=False)
    op.bulk_insert(tables.get('physical_address'),
                   load_json(os.path.join(seed_data, 'physical_address.json')),
                   multiinsert=False)
    op.bulk_insert(tables.get('service'),
                   load_json(os.path.join(seed_data, 'service.json')),
                   multiinsert=False)
    op.bulk_insert(tables.get('service_location'),
                   load_json(os.path.join(seed_data, 'service_location.json')),
                   multiinsert=False)

def downgrade():
    op.execute('DELETE FROM service_location')
    op.execute('DELETE FROM service')
    op.execute('DELETE FROM physical_address')
    op.execute('DELETE FROM program')
    op.execute('DELETE FROM location')
    op.execute('DELETE FROM organization')
    op.execute('DELETE FROM prerequisite')
    op.execute('DELETE FROM potential_outcome')
    op.execute('DELETE FROM format')
    op.execute('DELETE FROM entity_type')
    
