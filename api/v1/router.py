# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api

from .endpoints import *


api_blueprint = Blueprint('reg_api', __name__)
reg_api = Api(api_blueprint)

reg_api.add_resource(ProgramsResource, '/programs', 
                                    '/programs?id=<int:id>',
                                    '/programs?cip=<int:cip>')
reg_api.add_resource(ServicesResource, '/services', 
                                    '/services?id=<int:id>',
                                    '/services?location_id=<int:location_id>',
                                    '/services?location=<string:location>')