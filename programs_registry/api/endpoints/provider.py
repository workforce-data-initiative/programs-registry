# -*- coding: utf-8 -*-

"""
Flask-restful endpoint functions for Programs Registry PROVIDER (ORGANIZATION) resources

Request arguments are passed through webargs.flaskparser.use_args (decorator),
read from the specified locations and injected into the the GET, POST, PUT or DELETE.
Respective Marshmallow schema (in .schemas) is used to serialize/de-serialize registry 
objects created and queried.

NOTE: For POST/PUT, because an existing one isn't found on load, new instance of the model 
object is created from the args passed and injected into the function

TODO: add schema level validations for args

"""

from http import HTTPStatus
from flask_restful import Resource, abort 
from webargs.flaskparser import use_args

from common.utils import create_response, parse_args
from programs_registry.api.v1.models import db, Organization, Program, Service
from programs_registry.api.v1.schemas import OrganizationSchema, OrganizationPostSchema, \
                                            OrganizationProgramSchema, OrganizationServiceSchema, \
                                            ProgramPostSchema, ServicePostSchema


__all__ = ['ProviderResource',
           'ProviderProgramResource',
           'ProviderServiceResource',
           'ProviderLocationResource']


class ProviderResource(Resource):
    """
    Providers endpoint: uses the Organization model 
    to align with HSDS nomenclature 
    
    GET,POST /providers
    GET,PUT,DELETE /providers/id
    GET /providers?name=provider_name
    
    """
    
    @use_args(OrganizationSchema(), locations=('view_args', 'query'))
    def get(self, *args, **kwargs):
        request_args = parse_args(args, kwargs)
        organizations = Organization.get_by(request_args)
        
        if organizations:
            return create_response(organizations, OrganizationSchema(many=True), HTTPStatus.OK)

        abort(HTTPStatus.NOT_FOUND, message="None found: provider with {}".format(request_args))

    @use_args(OrganizationPostSchema(), locations=('json', 'form'))
    def post(self, *args):
        try:
            if args: 
                org = args[0]
                org.save()
                return create_response(org, OrganizationSchema(), HTTPStatus.CREATED)
            else:
                abort(HTTPStatus.NO_CONTENT, message="Nil or invalid provider organization data passed")
            
        except Exception as err:
            abort(HTTPStatus.BAD_REQUEST, message=err)

    @use_args(OrganizationPostSchema(), locations=('view_args', 'json', 'form'))     
    def put(self, *args, **kwargs):
        org_matches = Organization.get_by({'id': kwargs.get('organization_id')})

        if org_matches:
            org = org_matches.pop()
            
            for arg in args:    
                for key, value in arg.items():
                    if key is not 'id':
                        setattr(org, key, value) 
                org.save()
            return create_response(org, OrganizationSchema(), HTTPStatus.ACCEPTED)
        else:
            abort(HTTPStatus.NOT_FOUND, message="None found: provider organization id={}".format(kwargs.get('organization_id')))
                
        return create_response(args, OrganizationSchema(), HTTPStatus.NOT_MODIFIED)
    
    
    def delete(self, organization_id):
        try:
            org_matches = Organization.get_by({'id': organization_id})
        
            if org_matches:
                org = org_matches.pop()
                org.delete()
                deleted = "Successfully deleted: organization {}".format(organization_id)
                return create_response({"message": deleted}, schema=None, status=HTTPStatus.ACCEPTED)
            else:
                abort(HTTPStatus.NOT_FOUND, message="None found: provider with id {}".format(organization_id))
                
        except Exception as err:
            abort(HTTPStatus.NOT_MODIFIED, message=err)


class ProviderProgramResource(Resource):
    """
    Provider programs endpoint
    
    GET,POST /providers/<organization_id>/programs
    GET,PUT,DELETE providers/<organization_id>/programs/<id>
    
    """
    
    @use_args(OrganizationProgramSchema(), locations=('view_args', 'query'))
    def get(self, *args, **kwargs):
        request_args = parse_args(args, kwargs)
        provider_programs = Program.get_by(request_args)
        
        if provider_programs:
            return create_response(provider_programs, OrganizationProgramSchema(many=True), HTTPStatus.OK)

        abort(HTTPStatus.NOT_FOUND, message="None found: provider with {}".format(request_args))
    
    @use_args(ProgramPostSchema(), locations=('view_args', 'json', 'form'))  
    def post(self, *args, **kwargs):
        try:
            if args:
                program = args[0]
                program.save()
                return create_response(program, OrganizationProgramSchema(), HTTPStatus.CREATED)
            else:
                abort(HTTPStatus.NO_CONTENT, message="Nil or invalid provider program data passed")
                
        except Exception as err:
            abort(HTTPStatus.BAD_REQUEST, message=err)
    
    @use_args(ProgramPostSchema(), locations=('view_args', 'json', 'form'))   
    def put(self, *args, **kwargs):
        prog_matches = Program.get_by(kwargs)
    
        if prog_matches:
            prog = prog_matches.pop()
                
            for arg in args:
                for key, value in arg.items():
                    if key is not 'id':
                        setattr(prog, key, value)
        
            prog.save()
            return create_response(prog, OrganizationProgramSchema(), HTTPStatus.ACCEPTED)
        else:
            abort(HTTPStatus.NOT_FOUND, message="None found: program id {} from provider id {}".format(kwargs.get('program_id'),
                                                                                                       kwargs.get('organization_id')))
    
    def delete(self, organization_id, program_id):
        try:
            prog_matches = Program.get_by({'id': program_id, 
                                           'organization_id': organization_id})
            
            if prog_matches:
                prog = prog_matches.pop()
                prog.delete()
                deleted = "Successfully deleted: program id {} from provider id {}".format(program_id, organization_id)
                return create_response({"message": deleted}, schema=None, status=HTTPStatus.ACCEPTED)
            else:
                abort(HTTPStatus.NOT_FOUND, message="None found: program id {} from provider id {}".format(program_id,
                                                                                                        organization_id))
                
        except Exception as err:
            abort(HTTPStatus.NOT_MODIFIED, message=err)


class ProviderServiceResource(Resource):
    """
    Provider services endpoint
    
    GET,POST /providers/<organization_id>/services
    GET,PUT,DELETE /providers/<organization_id>/services/<service_id>
    GET /providers/<organization_id>/services?
    
    """
    
    @use_args(OrganizationServiceSchema(), locations=('view_args', 'query'))
    def get(self, *args, **kwargs):
        request_args = parse_args(args, kwargs)
        provider_services = Service.get_by(request_args)
         
        if provider_services:
            return create_response(provider_services, OrganizationServiceSchema(many=True), HTTPStatus.OK)
 
        abort(HTTPStatus.NOT_FOUND, message="None found: provider with {}".format(request_args))
    
    @use_args(ServicePostSchema(), locations=('view_args', 'json', 'form'))  
    def post(self, *args, **kwargs):
        try:
            if args:
                service = args[0]
                service.save()
                return create_response(service, OrganizationServiceSchema(), HTTPStatus.CREATED)
            else:
                abort(HTTPStatus.NO_CONTENT, message="Nil or invalid provider service data passed")
                
        except Exception as err:
            abort(HTTPStatus.BAD_REQUEST, message=err)
    
    @use_args(ServicePostSchema(), locations=('view_args', 'json', 'form'))   
    def put(self, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        service_matches = Service.get_by(kwargs)
    
        if service_matches:
            service = service_matches.pop()
                
            for arg in args:
                for key, value in arg.items():
                    if key is not 'id':
                        setattr(service, key, value)
        
            service.save()
            return create_response(service, OrganizationServiceSchema(), HTTPStatus.ACCEPTED)
        else:
            abort(HTTPStatus.NOT_FOUND, message="None found: service id {} from provider id {}".format(kwargs.get('service_id'),
                                                                                                       kwargs.get('organization_id')))
    def delete(self, organization_id, service_id):
        try:
            service_matches = Service.get_by({'id': service_id, 
                                           'organization_id': organization_id})
            
            if service_matches:
                service = service_matches.pop()
                service.delete()
                deleted = "Successfully deleted: service id {} from provider id {}".format(service_id, organization_id)
                return create_response({"message": deleted}, schema=None, status=HTTPStatus.ACCEPTED)
            else:
                abort(HTTPStatus.NOT_FOUND, message="None found: service id {} from provider id {}".format(service_id,
                                                                                                        organization_id))
                
        except Exception as err:
            abort(HTTPStatus.NOT_MODIFIED, message=err)


class ProviderLocationResource(Resource):
    pass