# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from instance.config import app_config


db = SQLAlchemy()
ma = Marshmallow()   
    
def openapi_spec():
    import connexion
    return connexion.App(__name__).add_api('../openapi.yaml')
    
def create_app():
    config_name = os.getenv('APP_SETTINGS', 'instance.config.DevelopmentConfig')

    if 'production' in config_name.lower():
        app = Flask(__name__, instance_relative_config=True) 
    else:
        app = openapi_spec()
    
    app.config.from_object(app_config.get(config_name))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # note: initialize SQLAlchemy before Marshmallow
    db.init_app(app)
    ma.init_app(app)
    
    from api.v1.router import api_blueprint as api_blueprint_v1
    app.register_blueprint(api_blueprint_v1, url_prefix='/api/v1')
    
    return app
