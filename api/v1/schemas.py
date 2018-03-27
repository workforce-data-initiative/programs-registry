# -*- coding: utf-8 -*-

from webargs.flaskparser import use_args

from app.app import ma
from .models import *


class PhysicalAddressSchema(ma.ModelSchema):
    class Meta:
        model = PhysicalAddress


class OrganizationSchema(ma.ModelSchema):
    class Meta:
        model = Organization
        #strict = True
    
    locations = ma.Nested('LocationSchema', many=True, exclude=('organization', 'services'))
    #programs =
    #services =
 

class LocationSchema(ma.ModelSchema):
    class Meta:
        model = Location
    
    organization = ma.Nested(OrganizationSchema, exclude=('locations',))
    address = ma.Nested(PhysicalAddressSchema)
    services = ma.Nested('ServiceSchema', many=True)


class ServiceSchema(ma.ModelSchema): 
    class Meta:
        model = Service
    
    program = ma.Nested('ProgramSchema', exclude=('services', 'organization'))
    organization = ma.Nested(OrganizationSchema, exclude=('programs', 'services', 'locations'))
    locations = ma.Nested(LocationSchema, many=True, exclude=('services', 'organization'))
    #TODO: fix so provider location(s) == service locations

   
class ProgramSchema(ma.ModelSchema):    
    class Meta:
        model = Program
    
    organization = ma.Nested(OrganizationSchema, exclude=('programs', 'services', 'locations'))  
    services = ma.Nested(ServiceSchema, many=True, exclude=('program', 'organization'))
