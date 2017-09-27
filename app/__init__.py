# app/__init__.py
import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

from instance.config import app_config

# initialize db
db = SQLAlchemy()


def create_app(config_name):

    from app.models import Program

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    # define the routes for the service
    @app.route('/programs/', methods=['POST', 'GET'])
    def bucketlists():
        response = {}
        return make_response(jsonify(response), 200)

    return app
