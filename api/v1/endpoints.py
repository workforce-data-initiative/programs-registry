# -*- coding: utf-8 -*-

from http import HTTPStatus
from flask_restful import Resource, abort, request 
from webargs.flaskparser import use_args

from common.utils import create_response, get_payload
from .models import *
from .schemas import *


class ProvidersResource(Resource):
    """Providers endpoint; this uses the Organization model
    to align with HSDS nomenclature 
    
    GET,POST /providers
    GET,PUT,DELETE /providers?id=1
    GET /providers?name=provider_name
    """
    
    @use_args(OrganizationSchema(), locations=('query',))
    def get(self, args):
        if not args:
            organizations = Organization.get_all()
        else:
            organizations = Organization.get_by(args)
        
        if organizations:
            return create_response(organizations, OrganizationSchema(many=True), HTTPStatus.OK)

        abort(HTTPStatus.NOT_FOUND, message="No matching provider found")

    @use_args(OrganizationSchema(), locations=('json', 'form'))
    def post(self, provider_organization):
        try:
            provider_organization.save()
            return create_response(org, OrganizationSchema(), HTTPStatus.CREATED)
        
        except Exception as e:
            abort(HTTPStatus.BAD_REQUEST, message=str(e))
    
    @use_args(OrganizationSchema(), locations=('query', 'json', 'form'))     
    def put(self, args):
        # TODO: test for case where you try a put on organization that doesn't exist
        org_matches = Organization.get_by({'id': args.get('id')})
        
        if org_matches:
            org = org_matches.pop()
            try:
                for key, value in get_payload(request).items():
                    setattr(org, key, value)
                    
                org.save()
                return create_response(org, OrganizationSchema(), HTTPStatus.ACCEPTED)
            
            except Exception as e:
                abort(HTTPStatus.NOT_MODIFIED, message=str(e))
        else:
            abort(HTTPStatus.NOT_FOUND, message="None found: provider with id {}".format(args.get('id')))
            
    @use_args(OrganizationSchema(), locations=('query',))
    def delete(self, args):
        org_matches = Organization.get_by(args)
        
        if org_matches:
            org = org_matches.pop()
            try:
                org.delete()
                delete_notification = "Successfully deleted: organization {}".format(args.get('id'))
                return create_response({"message": delete_notification}, schema=None, status=HTTPStatus.ACCEPTED)
            
            except Exception as e:
                abort(HTTPStatus.NOT_MODIFIED, message=str(e))
        else:
            abort(HTTPStatus.NOT_FOUND, message="None found: provider with id {}".format(args.get('id')))


class ProgramsResource(Resource):
    """Programs endpoint
    
    GET,POST /programs
    GET,PUT,DELETE /programs?id=1
    GET /programs?name=program_name
    GET /programs?cip=12345
    """
    
    @use_args(ProgramSchema(), locations=('query',))
    def get(self, args): 
        if not args:
            programs = Program.get_all()
        else:
            programs = Program.get_by(args)
        
        if programs:
            return create_response(programs, ProgramSchema(many=True), HTTPStatus.OK)

        abort(HTTPStatus.NOT_FOUND, message="No matching programs found")

    @use_args(ProgramPostSchema(), locations=('json', 'form'))
    def post(self, program):
        org_matches = Organization.get_by({'id': program.organization_id})
        
        if org_matches:
            try:
                program.save()
                return create_response(program, ProgramSchema(), HTTPStatus.CREATED)
         
            except Exception as e:
                abort(HTTPStatus.BAD_REQUEST, message=str(e))
        else:
            not_found = "None found: provider organization with id {}. Create this provider organization before adding programs".format(program.organization_id)
            abort(HTTPStatus.NOT_FOUND, message=not_found)
    
     
class ServicesResource(Resource):
    """Services endpoint
    
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

class PhysicalAddressResource(Resource):
    pass
                
                
                
                
                
                
                
                
                
                
                