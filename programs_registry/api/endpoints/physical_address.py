# -*- coding: utf-8 -*-

"""
Flask-restful endpoint functions for Programs Registry PHYSICALADDRESS resources

Request arguments are passed through webargs.flaskparser.use_args (decorator),
read from the specified locations and injected into the the GET, POST, PUT or DELETE.
Respective Marshmallow schema (in .schemas) is used to serialize/de-serialize registry 
objects created and queried.

NOTE: For POST/PUT, because an existing one isn't found on load, new instance of the model 
object is created from the args passed and injected into the function

TODO: add schema level validations for args

"""


from programs_registry.api.models import db, PhysicalAddress


class PhysicalAddressResource(Resource):
    def post(self):
        pass
    
    def put(self):
        pass

