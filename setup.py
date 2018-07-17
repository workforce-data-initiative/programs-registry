# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='programs_registry',
    version='0.1',
    packages=['programs_registry'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==1.0.2',
        'Flask-API==1.0',
        'Flask-Migrate==2.1.1',
        'Flask-SQLAlchemy==2.3.2',
        'Flask-Script==2.0.6',
        'flask-restful==0.3.6',
        'flask-marshmallow==0.8.0',
        'marshmallow-sqlalchemy==0.13.2',
        'psycopg2-binary==2.7.4',
        'connexion==1.4.2',
        'webargs==3.0.0'
    ],
    entry_points={
        'flask.commands': [
            'test=programs_registry.commands:test'
            ]
        }
)

