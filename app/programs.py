from flask import Blueprint, make_response, request, jsonify
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
                    'organization_id': organization_id,
                    'name': program.name,
                }
                if program.alternate_name:
                    response['alternate_name'] = program.alternate_name

                return make_response(jsonify(response)), 201

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
