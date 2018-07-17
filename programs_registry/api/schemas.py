# -*- coding: utf-8 -*-

from datetime import datetime, date
from marshmallow.decorators import pre_load
from flask_marshmallow import Marshmallow

from .models import *


ma = Marshmallow() 

# ---------------------------
# JSON dump schemas - GET
# ---------------------------
class EntityTypeSchema(ma.ModelSchema):
    class Meta:
        model = EntityType


class PotentialOutcomeSchema(ma.ModelSchema):
    class Meta:
        model = PotentialOutcome


class PrerequisiteSchema(ma.ModelSchema):
    class Meta:
        model = Prerequisite


class FormatSchema(ma.ModelSchema):
    class Meta:
        model = Format
        

class OrganizationSchema(ma.ModelSchema):
    class Meta:
        model = Organization
        exclude = ('organization_id',)
    
    entity_type = ma.Nested(EntityTypeSchema, exclude=('organizations',))
    locations = ma.Nested('LocationSchema', many=True, exclude=('organization', 'services'))
    programs = ma.Nested('ProgramSchema', many=True, exclude=('organization',))
    services = ma.Nested('ServiceSchema', many=True, exclude=('organization',))
    

class ProgramSchema(ma.ModelSchema): 
    class Meta:
        model = Program
        exclude = ('program_id',)
    
    potential_outcome = ma.Nested(PotentialOutcomeSchema, exclude=('programs',)) 
    prerequisite = ma.Nested(PrerequisiteSchema, exclude=('programs',)) 
    organization = ma.Nested(OrganizationSchema, exclude=('programs', 'services', 'locations'))  
    services = ma.Nested('ServiceSchema', many=True, exclude=('program', 'organization'))


class OrganizationProgramSchema(ma.ModelSchema):
    class Meta:
        model = Program
        exclude = ('program_id',)
    
    potential_outcome = ma.Nested(PotentialOutcomeSchema, exclude=('programs',)) 
    prerequisite = ma.Nested(PrerequisiteSchema, exclude=('programs',)) 
    services = ma.Nested('ServiceSchema', many=True, exclude=('program', 'organization'))


class OrganizationServiceSchema(ma.ModelSchema):
    class Meta:
        model = Service
        exclude = ('service_id',)

    format = ma.Nested(FormatSchema, exclude=('services',))
    locations = ma.Nested('LocationSchema', many=True, exclude=('services', 'organization'))


class ServiceSchema(ma.ModelSchema): 
    class Meta:
        model = Service
        exclude = ('service_id',)

    format = ma.Nested(FormatSchema, exclude=('services',))
    program = ma.Nested('ProgramSchema', exclude=('services', 'organization'))
    organization = ma.Nested(OrganizationSchema, exclude=('programs', 'services', 'locations'))
    locations = ma.Nested('LocationSchema', many=True, exclude=('services', 'organization'))


class LocationSchema(ma.ModelSchema):
    class Meta:
        model = Location
    
    organization = ma.Nested(OrganizationSchema, exclude=('locations',))
    physical_address = ma.Nested('PhysicalAddressSchema')
    services = ma.Nested(ServiceSchema, many=True)
    

class PhysicalAddressSchema(ma.ModelSchema):
    class Meta:
        model = PhysicalAddress

        
# --------------------------------
# JSON load schemas - POST/PUT
# --------------------------------
class OrganizationPostSchema(ma.ModelSchema):
    class Meta:
        model = Organization
        exclude = ('organization_id',)
        sqla_session = db.session
    
    #TODO: fix error with date parsing in POST/PUT
    @pre_load
    def parse_date(self, args):
        if 'year_incorporated' in args and isinstance(args.get('year_incorporated'), str):
            date_arg = datetime.strptime(args.get('year_incorporated'), '%Y-%m-%d')
            args['year_incorporated'] = date_arg.date()
        return args
    

class ProgramPostSchema(ma.ModelSchema):
    class Meta:
        model = Program
        exclude = ('program_id',)
        include_fk = True
        sqla_session = db.session


class ServicePostSchema(ma.ModelSchema):
    class Meta:
        model = Service
        exclude = ('service_id',)
        include_fk = True
        sqla_session = db.session
    