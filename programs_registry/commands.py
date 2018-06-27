# -*- coding: utf-8 -*-

import os
import click
from click import UsageError
from flask_migrate.cli import db

from . import create_app


config_name = os.environ.get('FLASK_ENV')
app = create_app(config_name)
test_root = os.path.join(app.root_path, 'tests')
_groups = ['models', 'endpoints']

def run_tests(test_dir):
    """Run unit tests without test coverage."""
    
    from unittest import TestLoader, TextTestRunner
    
    pattern = 'test_*.py'
    try:
        # First, find and discover all tests modules from the directory
        tests = TestLoader().discover(test_dir, pattern=pattern)
        result = TextTestRunner().run(tests)
    except Exception as err:
        raise
    
    return result

@app.cli.command()
@click.option('--all', is_flag=True, help='Run all tests.')
@click.argument('groups', required=False, 
                metavar='[GROUPS]({})'.format(','.join(_group for _group in _groups)))
def test(all, groups):
    """Run either all tests from one or more specified groups\n
    e.g: flask test --all\n
         flask test endpoints models
    """
    
    from unittest import TestLoader, TextTestRunner
    
    if all:
        result = run_tests(test_root)
        0 if result.wasSuccessful() else 1
    else:
        results = []
        test_groups = groups.split(',')
        
        for group in test_groups:
            if group in _groups:
                result = run_tests(os.path.join(test_root, group))
                results.append(result)
            else:
                message='Run flask test --help for usage information'
                raise click.UsageError(message)

        for result in results:
            if not result.wasSuccessful():
                return 1
        
        return 0
