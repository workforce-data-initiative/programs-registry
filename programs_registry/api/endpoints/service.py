# -*- coding: utf-8 -*-

"""
Flask-restful endpoint functions for Programs Registry SERVICE resources

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
from programs_registry.api.models import db, Service
from programs_registry.api.schemas import ServiceSchema, ServicePostSchema


__all__ = ['ServiceResource',
           'ServiceLocationResource']


class ServiceResource(Resource):
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
            

class ServiceLocationResource(Resource):
    pass