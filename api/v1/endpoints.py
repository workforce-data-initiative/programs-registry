# -*- coding: utf-8 -*-

from flask import jsonify, make_response
from flask_restful import Resource, Api, abort 

from .models import *
from .schemas import *
from common.utils import create_response

class OrganizationsResource(Resource):
    pass


class ProgramsResource(Resource):
    """Programs endpoint
    
    E.g:
    GET /programs
    GET /programs?id=1
    GET /programs?cip=12345
    """
    
    def __get(self, args):  
        if not args:
            return Program.query.all() 
        
        if 'id' in args:
            return Program.query.filter_by(id = args.get('id'))
        if 'cip' in args:
            return Program.query.filter_by(cip = args.get('cip'))
     
    @use_args_with(ProgramSchema)   
    def get(self, args):    
        programs = self.__get(args)
        if programs:
            return create_response(programs, ProgramSchema(many=True), 200)
        
        abort(404, message="No matching programs found")

    def post(self):
        pass
                
class ServicesResource(Resource):
    """Services endpoint
    
    E.g:
    GET /services
    GET /services?id=1
    GET /services?location_id=1
    GET /services?location=city
    """
    
    def __get(self, args):
        if not args:
            return Service.query.all()
        
        if 'id' in args:
            return Service.query.filter_by(id = args.get('id'))
        if 'location_id' in args:
            return Service.query.join(ServiceLocation).filter(
                                    ServiceLocation.location_id == args.get('location_id'))
        if 'location' in args:
            return Service.query.join(Service.locations).filter(
                                    Location.name.ilike("{}%".format(args.get('location')))).all()
 
    @use_args_with(ServiceSchema)
    def get(self, args):
        services = self.__get(args)
        if services:
            return create_response(services, ServiceSchema(many=True), 200)

        abort(404, message="No matching services found")
           
    @use_args_with(ServiceSchema)
    def post(self, args):
        #TODO: add the field validations
        pass


class LocationsResource(Resource):
    pass
                
                
                
                
                
                
                
                
                
                
                