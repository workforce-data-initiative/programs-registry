# -*- coding: utf-8 -*-

"""
Flask-restful endpoint functions for Programs Registry PROGRAM resources

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

from common.utils import create_response
from program_registry.api.v1.models import db, Program
from program_registry.api.v1.schemas import ProgramSchema, ProgramPostSchema


__all__ = ['ProgramResource',
           'ProgramServiceResource']


class ProgramResource(Resource):
    """Programs endpoint
    
    GET,POST /programs
    GET,PUT,DELETE /programs/id
    GET /programs?name=program_name
    GET /programs?cip=12345
    """
    
    @use_args(ProgramSchema(), locations=('view_args', 'query'))
    def get(self, *args, **kwargs): 
        filters = {}
        if kwargs:
            filters = kwargs
        else:
            for arg in args:
                filters.update(arg)
                
        programs = Program.get_by(filters)
        
        if programs:
            return create_response(programs, ProgramSchema(many=True), HTTPStatus.OK)

        abort(HTTPStatus.NOT_FOUND, message="No matching programs found: {}".format(filters))

    @use_args(ProgramPostSchema(), locations=('view_args', 'json', 'form'))
    def post(self, *args):
        try:
            if args:
                program = args[0]
                program.save()
                return create_response(program, ProgramSchema(), HTTPStatus.CREATED)
            else:
                abort(HTTPStatus.NO_CONTENT, message="Nil or invalid program data passed")
                
        except Exception as err:
            abort(HTTPStatus.BAD_REQUEST, message=err)

    @use_args(ProgramPostSchema(), locations=('view_args', 'json', 'form'))   
    def put(self, *args, **kwargs):
        program_matches = Program.get_by(kwargs)
    
        if program_matches:
            program = program_matches.pop()
                
            for arg in args:
                for key, value in arg.items():
                    if key is not 'id':
                        setattr(program, key, value)
        
            program.save()
            return create_response(program, ProgramSchema(), HTTPStatus.ACCEPTED)
        else:
            abort(HTTPStatus.NOT_FOUND, message="None found: program with id {}".format(kwargs.get('program_id')))
                
        return create_response(args, ProgramSchema(), HTTPStatus.NOT_MODIFIED)

    def delete(self, program_id):
        try:
            program_matches = Program.get_by({'id': program_id})
        
            if program_matches:
                program = program_matches.pop()
                program.delete()
                deleted = "Successfully deleted: program {}".format(program_id)
                return create_response({"message": deleted}, schema=None, status=HTTPStatus.ACCEPTED)
            else:
                abort(HTTPStatus.NOT_FOUND, message="None found: program with id {}".format(program_id))
                
        except Exception as err:
            abort(HTTPStatus.NOT_MODIFIED, message=err)
        

class ProgramServiceResource(Resource):
    pass
