from flask import Blueprint, make_response, request, jsonify, abort
from flask.views import MethodView

from app.models import Program


program_blueprint = Blueprint('program', __name__)


class ProgramView(MethodView):
    """
    This class handles api requests for the program resource.
    /api/organizations/<org_id>/programs - GET
    /api/organizations/<org_id>/programs - POST
    /api/organizations/<org_id>/programs/<id> - PUT
    /api/organizations/<org_id>/programs/<id> - DELETE
    """

    def post(self, organization_id):
        """
        Create a program and return a json response containing it.
        """
        try:
            payload = request.data.to_dict()
            if organization_id is not None:
                payload['organization_id'] = organization_id
                program = Program(**payload)
                program.save()

                response = {
                    'id': program.id,
                    'organization_id': program.organization_id,
                    'name': program.name,
                }
                if program.alternate_name:
                    response['alternate_name'] = program.alternate_name

                return make_response(jsonify(response)), 201
            else:
                abort(404)

        except Exception as e:
            response = { "message": str(e) }
            return make_response(jsonify(response)), 400


    def get(self, organization_id, program_id):
        """
        Get an existing program(s) and return as a json response
        """
        if program_id is not None:
                # handle the get by id
            try:
                program = Program.query.filter_by(id=program_id).first()
                response = {
                    'id': program.id,
                    'name': program.name,
                    'organization_id': program.organization_id,
                }
                return make_response(jsonify(response)), 200

            except Exception as e:
                response = { "message": str(e) }
                return make_response(jsonify(response)), 400
        else:
            # handle get all
            programs = Program.get_all()
            response = []

            for prog in programs:
                single_prog = {
                    'id': prog.id,
                    'name': prog.name,
                    'organization_id': prog.organization_id
                }
                response.append(single_prog)
                return make_response(jsonify(response)), 200

    def put(self, organization_id, program_id):
        """Update an existing program and return a json response."""

        if program_id is not None:
            try:
                response = {}
                program = Program.query.filter_by(id=program_id).first()
                response['id'] = program.id

                if 'name' in request.data:
                    program.name = request.data.get('name')
                if 'alternate_name' in request.data:
                    program.alternate_name = request.data.get('alternate_name')
                program.save()

                response['organization_id'] = program.organization_id
                response['name'] = program.name

                return make_response(jsonify(response)), 200

            except Exception as e:
                response = { "message": str(e) }
                return make_response(jsonify(response)), 400
        else:
            abort(404)

    def delete(self, organization_id, program_id):
        """Delete a program given its id."""

        if program_id is not None:
            try:
                prog = Program.query.filter_by(id=program_id).first()
                prog.delete()

                return make_response(jsonify({})), 202

            except Exception as e:
                response = { "message": str(e) }
                return make_response(jsonify(response)), 400



program_view = ProgramView.as_view('program_view')
program_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/programs/',
    view_func=program_view,
    methods=['POST'])
program_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/programs/',
    view_func=program_view, defaults={'program_id': None},
    methods=['GET'])
program_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/programs/<int:program_id>',
    view_func=program_view,
    methods=['GET', 'PUT', 'DELETE'])
