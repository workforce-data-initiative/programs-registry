# -*- coding: utf-8 -*-

"""
Flask-restful endpoint functions for programs registry resources

Request arguments are passed through webargs.flaskparser.use_args (decorator),
read from the specified locations and injected into the the GET, POST, PUT or DELETE.
Respective Marshmallow schema (in .schemas) is used to serialize/de-serialize registry 
objects created and queried.

For POST/PUT, because an existing one isn't found on load, new instance of the model 
object is created from the args passed and injected into the function

TODO: add schema level validations for args

"""

from http import HTTPStatus
from flask_restful import Resource, abort 
from webargs.flaskparser import use_args

from common.utils import create_response
from .models import *
from .schemas import *


class ProvidersResource(Resource):
    """Providers endpoint; this uses the Organization 
    model to align with HSDS nomenclature 
    
    GET,POST /providers
    GET,PUT,DELETE /providers?id=1
    GET /providers?name=provider_name
    """
    
    @use_args(OrganizationSchema(), locations=('query',))
    def get(self, organization_id, args):
        if not (organization_id and args):
            organizations = Organization.get_all()
        elif organization_id:
            organizations = Organization.get_by({'id': organization_id})
        else:
            organizations = Organization.get_by(args)
        
        if organizations:
            return create_response(organizations, OrganizationSchema(many=True), HTTPStatus.OK)

        abort(HTTPStatus.NOT_FOUND, message="No matching provider found: {}".format(args))

    @use_args(OrganizationPostSchema(), locations=('json', 'form'))
    def post(self, args):
        try:
            if args:    
                org = args
                org.save()
                return create_response(org, OrganizationSchema(), HTTPStatus.CREATED)
            else:
                abort(HTTPStatus.NO_CONTENT, message="Nil or invalid provider organization data passed")
            
        except Exception as e:
            abort(HTTPStatus.BAD_REQUEST, message=str(e))

    @use_args(OrganizationPostSchema(), locations=('query', 'json', 'form'))     
    def put(self, args):
        try:
            org_matches = Organization.get_by({'id': args.get('id')})
            
            if org_matches:
                org = org_matches.pop()
                for key, value in args.items():
                    if key is not 'id':
                        setattr(org, key, value) 
                org.save()
                return create_response(org, OrganizationSchema(), HTTPStatus.ACCEPTED)
            else:
                abort(HTTPStatus.NOT_FOUND, message="None found: provider with id {}".format(args.get('id')))
                
        except Exception as err:
            abort(HTTPStatus.NOT_MODIFIED, message=err)
            
    @use_args(OrganizationSchema(), locations=('query',))
    def delete(self, args):
        try:
            org_matches = Organization.get_by(args)
        
            if org_matches:
                org = org_matches.pop()
                org.delete()
                deleted = "Successfully deleted: organization {}".format(args.get('id'))
                return create_response({"message": deleted}, schema=None, status=HTTPStatus.ACCEPTED)
            else:
                abort(HTTPStatus.NOT_FOUND, message="None found: provider with id {}".format(args.get('id')))
                
        except Exception as err:
            abort(HTTPStatus.NOT_MODIFIED, message=err)


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

        abort(HTTPStatus.NOT_FOUND, message="No matching programs found: {}".format(args))

    @use_args(ProgramPostSchema(), locations=('json', 'form'))
    def post(self, args):
        try:
            if args:
                program = args
                program.save()
                return create_response(program, ProgramSchema(), HTTPStatus.CREATED)
            else:
                abort(HTTPStatus.NO_CONTENT, message="Nil or invalid program data passed")
                
        except Exception as err:
            abort(HTTPStatus.BAD_REQUEST, message=err)

    @use_args(ProgramPostSchema(), locations=('query', 'json', 'form'))   
    def put(self, args):
        try:
            program_matches = Program.get_by({'id': args.get('id')})
    
            if program_matches:
                program = program_matches.pop()
                for key, value in args.items():
                    if key is not 'id':
                        setattr(program, key, value)
        
                program.save()
                return create_response(program, ProgramSchema(), HTTPStatus.ACCEPTED)
            else:
                abort(HTTPStatus.NOT_FOUND, message="None found: program with id {}".format(args.get('id')))
                
        except Exception as err:
            abort(HTTPStatus.NOT_MODIFIED, message=err)

    @use_args(ProgramSchema(), locations=('query',))
    def delete(self, args):
        try:
            program_matches = Program.get_by(args)
        
            if program_matches:
                program = program_matches.pop()
                program.delete()
                deleted = "Successfully deleted: program {}".format(args.get('id'))
                return create_response({"message": deleted}, schema=None, status=HTTPStatus.ACCEPTED)
            else:
                abort(HTTPStatus.NOT_FOUND, message="None found: program with id {}".format(args.get('id')))
                
        except Exception as err:
            abort(HTTPStatus.NOT_MODIFIED, message=err)
        

class ServicesResource(Resource):
    """Services endpoint
    
    GET,POST /services
    GET,PUT,DELETE /services?id=1
    GET /services?status=deferred
    GET /services?name=service_name
    """
    
    @use_args(ServiceSchema(), locations=('query',))
    def get(self, args):
        if not args:
            services = Service.get_all()
        else:
            services = Service.get_by(args)
        
        if services:
            return create_response(services, ServiceSchema(many=True), HTTPStatus.OK)

        abort(HTTPStatus.NOT_FOUND, message="No matching services found: {}".format(args))
    
    @use_args(ServicePostSchema(), locations=('json', 'form'))
    def post(self, args):
        try:
            if args:
                service = args
                service.save()
                return create_response(service, ServiceSchema(), HTTPStatus.CREATED)
            else:
                abort(HTTPStatus.NO_CONTENT, message="Nil or invalid service data passed")
                
        except Exception as err:
            abort(HTTPStatus.BAD_REQUEST, message=err)
    
    @use_args(ServicePostSchema(), locations=('query', 'json', 'form'))
    def put(self, args):
        try:
            service_matches = Service.get_by({'id': args.get('id')})
    
            if service_matches:
                service = service_matches.pop()
                for key, value in args.items():
                    if key is not 'id':
                        setattr(service, key, value)
                        
                service.save()
                return create_response(service, ServiceSchema(), HTTPStatus.ACCEPTED)
            else:
                abort(HTTPStatus.NOT_FOUND, message="None found: service with id {}".format(args.get('id')))
                
        except Exception as err:
            abort(HTTPStatus.NOT_MODIFIED, message=err)
            
    @use_args(ServiceSchema(), locations=('query',))
    def delete(self, args):
        try:
            service_matches = Service.get_by(args)
        
            if service_matches:
                service = service_matches.pop()
                service.delete()
                deleted = "Successfully deleted: service {}".format(args.get('id'))
                return create_response({"message": deleted}, schema=None, status=HTTPStatus.ACCEPTED)
            else:
                abort(HTTPStatus.NOT_FOUND, message="None found: service with id {}".format(args.get('id')))
                
        except Exception as err:
            abort(HTTPStatus.NOT_MODIFIED, message=err)
        

class LocationsResource(Resource):
    pass

class PhysicalAddressResource(Resource):
    pass
                
                
                
                
                
                
                
                
                
                
                