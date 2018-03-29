# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api

from .endpoints import *


api_blueprint = Blueprint('reg_api', __name__)
reg_api = Api(api_blueprint)

reg_api.add_resource(ProgramsResource, '/programs', 
                                    '/programs?id=<int:id>',
                                    '/programs?cip=<int:cip>',
                                    '/programs?name=<string:name>')
reg_api.add_resource(ServicesResource, '/services', 
                                    '/services?id=<int:id>',
                                    '/services?status=<string:status>',
                                    '/services?name=<string:name>')
reg_api.add_resource(ProvidersResource, '/providers',
                                        '/providers?id=<int:id>',
                                        '/providers?name=<string:name>')