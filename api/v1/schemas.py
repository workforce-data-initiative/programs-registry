# -*- coding: utf-8 -*-

from datetime import datetime, date
from webargs.flaskparser import use_args
from marshmallow.decorators import pre_load, post_load

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
   
    @pre_load
    def parse_date(self, args):
        if 'year_incorporated' in args and isinstance(args.get('year_incorporated'), str):
            date_arg = datetime.strptime(args.get('year_incorporated'), '%Y-%m-%d')
            args['year_incorporated'] = date_arg.date()
        return args
 

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
    """Detailed dump schema"""

    class Meta:
        model = Program
    
    organization = ma.Nested(OrganizationSchema, exclude=('programs', 'services', 'locations'))  
    services = ma.Nested(ServiceSchema, many=True, exclude=('program', 'organization'))


class ProgramPostSchema(ma.ModelSchema):
    class Meta:
        model = Program
        include_fk = True
