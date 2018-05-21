# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='program_registry',
    packages=['program_registry'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==1.0.2',
    ],
    entry_points={
        'flask.commands': [
            'test=program_registry.commands:test'
            ]
        }
)