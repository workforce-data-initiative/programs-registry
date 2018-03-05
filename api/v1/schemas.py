# -*- coding: utf-8 -*-

from webargs.flaskparser import use_args
from marshmallow import fields

from .models import *
from app.app import ma

    
class OrganizationSchema(ma.ModelSchema):
    class Meta:
        model = Organization


class ServiceSchema(ma.ModelSchema):       
    class Meta:
        model = Service
        exclude = ['locations']
    

class LocationSchema(ma.ModelSchema):
    services = ma.Nested(ServiceSchema, many=True)
    
    class Meta:
        model = Location
 

class ProgramSchema(ma.ModelSchema):
    services = ma.Nested(ServiceSchema, many=True)
    
    class Meta:
        model = Program


class PhysicalAddressSchema(ma.ModelSchema):
    class Meta:
        model = PhysicalAddress


def use_args_with(schema_cls, schema_kwargs=None, **kwargs):
    """Reusable schema args decorator
    
    Credits: webargs docs
    Usage: @use_args_with(MySchema)
    """
    
    schema_kwargs = schema_kwargs or {}
    def factory(request):
        only = request.args.get('fields', default=None, type=None)
        partial = request.method == 'PATCH'
       
        # strict set to False since Marshmallow generated schemas expect required fields in args
        return schema_cls(only=only, partial=partial, strict=False,
                          context={'request': request}, **schema_kwargs)

    return use_args(factory, **kwargs)
