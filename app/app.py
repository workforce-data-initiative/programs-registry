# -*- coding: utf-8 -*-

# import os
from flask import Flask

from instance.config import app_config


def openapi_spec():
    import connexion
    return connexion.App(__name__).add_api('../openapi.yaml')


def create_app(config_name=None):
    #     if 'production' in config_name.lower():
    #         app = Flask(__name__, instance_relative_config=True)
    #     else:
    #         app = openapi_spec()
    app = Flask(__name__)
    app.config.from_object(app_config.get(config_name, 'development'))
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # IMPORTANT: initialize SQLAlchemy before Marshmallow
    from api.v1.models import db
    db.init_app(app)

    from api.v1.schemas import ma
    ma.init_app(app)

    from api.v1.router import api_blueprint as api_blueprint_v1
    app.register_blueprint(api_blueprint_v1, url_prefix='/api/v1')

    return app
