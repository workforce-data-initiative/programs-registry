# -*- coding: utf-8 -*-

import os
import unittest
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand

from api.v1.models import db
from app.app import create_app


config_name = os.environ.get('APP_SETTINGS', default='production')
app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)
# Define the migration command to always be prepended by the word "db"
# Example usage: python manage.py db init
manager.add_command('db', MigrateCommand)

class SeedDB(Command):
    """Seeds data from csv files to the DB"""
 
    def run(self):
        subprocess.call(['sh seed_data.sh'], shell=True)
 

@manager.command
def test():
    """Run the unit tests without test coverage."""
    
    # First, find and discover all tests modules from the directory
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner().run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
