# -*- coding: utf-8 -*-

from flask_restful import Resource, abort 
from webargs.flaskparser import use_args

from common.utils import create_response
from .models import *
from .schemas import *


class OrganizationsResource(Resource):
    @use_args(OrganizationSchema(), locations=('query',))
    def get(self, args):
        print(args)
        if not args:
            organizations = Organization.get_all()
        else:
            organizations = Organization.get_by(args)
        
        if organizations:
            print(organizations)
            return create_response(organizations, OrganizationSchema(many=True), 200)

        abort(404, message="No matching organizations found")


class ProgramsResource(Resource):
    """Programs endpoint
    
    E.g:
    GET /programs
    GET /programs?id=1
    GET /programs?name=program_name
    GET /programs?cip=12345
    """
    
    @use_args(ProgramSchema(), locations=('query',))
    def get(self, args): 
        """Get an existing program(s) and return as a json response
        """
        import ipdb; ipdb.set_trace()
        if not args:
            programs = Program.get_all()
        else:
            programs = Program.get_by(args)
        
        if programs:
            print(programs)
            return create_response(programs, ProgramSchema(many=True), 200)

        abort(404, message="No matching programs found")

#     @use_args(ProgramSchema(), locations=('json',))
#     def post(self, args):
#         print(args)
#         
#         if request.headers['Content-Type'] == "application/json":
#             payload = request.get_json(silent=True)
#         elif request.form:
#             payload = request.data.to_dict()
#         else:
#             payload = request.get_json(force=True)
#         
#         if Organization.get_by({'organization_id': payload['organization_id']}):
#             program = Program(**payload)
#             program.save()
#             return create_response(program, ProgramSchema(), 201)
#         else:
#             abort(404, message="No organization with id {} found".format(payload['organization_id']))

               
class ServicesResource(Resource):
    """Services endpoint
    
    E.g:
    GET /services
    GET /services?id=1
    GET /services?status=deferred
    TOFIX: GET /services?name=service_name
    """
    
    @use_args(ServiceSchema(), locations=('query',))
    def get(self, args):
        if not args:
            services = Service.get_all()
        else:
            services = Service.get_by(args=args)
        
        if services:
            return create_response(services, ServiceSchema(many=True), 200)

        abort(404, message="No matching services found")
    
    def post(self, args):
        #TODO: add the field validations
        pass


class LocationsResource(Resource):
    pass
                
                
                
                
                
                
                
                
                
                
                