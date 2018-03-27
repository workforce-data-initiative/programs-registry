# -*- coding: utf-8 -*-

from http import HTTPStatus
from flask_restful import Resource, abort, request 
from webargs.flaskparser import use_args

from common.utils import create_response, get_payload
from .models import *
from .schemas import *


class OrganizationsResource(Resource):
    """Providers endpoint
    
    GET/POST /providers
    GET /providers?id=1
    GET /providers?name=provider_name
    PUT/DELETE /providers?id=1
    """
    
    @use_args(OrganizationSchema())
    def get(self, args):
        if not args:
            organizations = Organization.get_all()
        else:
            organizations = Organization.get_by(args)
        
        if organizations:
            return create_response(organizations, OrganizationSchema(many=True), HTTPStatus.OK)

        abort(HTTPStatus.NOT_FOUND, message="None found: matching organization")

    @use_args(OrganizationSchema())
    def post(self, args):
        try:
            org = Organization(**get_payload(request))
            org.save()
            return create_response(org, OrganizationSchema(), HTTPStatus.CREATED)
        
        except Exception as e:
            abort(HTTPStatus.BAD_REQUEST, message=str(e))
    
    @use_args(OrganizationSchema())     
    def put(self, args):
        org = Organization.get_by({'id': args.get('id')}).pop()
        
        if org:
            try:
                for key, value in get_payload(request).items():
                    setattr(org, key, value)
                    
                org.save()
                return create_response(org, OrganizationSchema(), HTTPStatus.ACCEPTED)
            
            except Exception as e:
                abort(HTTPStatus.NOT_MODIFIED, message=str(e))
        else:
            abort(HTTPStatus.NOT_FOUND, message="None found: organization {}".format(args.get('id')))

    @use_args(OrganizationSchema())
    def delete(self, args):
        org = Organization.get_by({'id': args.get('id')}).pop()
                
        if org:
            try:
                org.delete()
                delete_notification = "Successfully deleted: organization {}".format(args.get('id'))
                return create_response({"message": delete_notification}, schema=None, status=HTTPStatus.ACCEPTED)
            except Exception as e:
                abort(HTTPStatus.NOT_MODIFIED, message=str(e))
        else:
            abort(HTTPStatus.NOT_FOUND, message="None found: organization {}".format(args.get('id')))


class ProgramsResource(Resource):
    """Programs endpoint
    
    GET /programs
    GET /programs?id=1
    GET /programs?name=program_name
    GET /programs?cip=12345
    """
    
    @use_args(ProgramSchema())
    def get(self, args): 
        """Get an existing program(s) and return as a json response
        """

        if not args:
            programs = Program.get_all()
        else:
            programs = Program.get_by(args)
        
        if programs:
            print(programs)
            return create_response(programs, ProgramSchema(many=True), 200)

        abort(404, message="No matching programs found")

               
class ServicesResource(Resource):
    """Services endpoint
    
    E.g:
    GET /services
    GET /services?id=1
    GET /services?status=deferred
    GET /services?name=service_name
    """
    
    @use_args(ServiceSchema())
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
                
                
                
                
                
                
                
                
                
                
                