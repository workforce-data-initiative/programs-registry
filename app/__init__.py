# app/__init__.py
import json
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

# initialize db
db = SQLAlchemy()


def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # import the blueprints and register it on the app

    from .organization import org_blueprint
    from .programs import program_blueprint
    from .services import service_blueprint
    from .locations import location_blueprint
    from .physical_address import address_blueprint

    app.register_blueprint(org_blueprint)
    app.register_blueprint(program_blueprint)
    app.register_blueprint(service_blueprint)
    app.register_blueprint(location_blueprint)
    app.register_blueprint(address_blueprint)
    return app
