# -*- coding: utf-8 -*-

import os
import click
from flask_migrate.cli import db

from . import create_app


config_name = os.environ.get('FLASK_ENV')
app = create_app(config_name)
test_root = os.path.join(app.root_path, 'tests')
    
@app.cli.command()
@click.argument('group')
def test(group):
    """Run unit tests without test coverage."""
    
    import unittest
    try:
        # First, find and discover all tests modules from the directory
        tests = unittest.TestLoader().discover(os.path.join(test_root, group), 
                                               pattern='test_*.py')
        result = unittest.TextTestRunner().run(tests)
        0 if result.wasSuccessful() else 1
    
    except Exception as err:
        raise err
    