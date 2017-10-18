from flask import Blueprint, make_response, request, jsonify, abort
from flask.views import MethodView

from app.models import Service


service_blueprint = Blueprint('service', __name__)


class ServiceView(MethodView):
    """
    This class handles api requests for the service resource.

    Accepted endpoints include:
    /api/organizations/<org_id>/programs/<program_id>/services/ - GET
    /api/organizations/<org_id>/programs/<program_id>/services/ - POST
    /api/organizations/<org_id>/programs/<program_id>/services/<id> - PUT
    /api/organizations/<org_id>/programs/<program_id>/services/<id> - DELETE
    """

    def post(self, organization_id, program_id):
        """
        Create a service and return a json response containing it.
        """
        try:
            payload = request.data.to_dict()
            if organization_id is not None:
                payload['organization_id'] = organization_id
                service = Service(**payload)
                service.save()
                response = service.serialize()
                return make_response(jsonify(response)), 201
            else:
                abort(404)

        except Exception as e:
            response = { "message": str(e) }
            return make_response(jsonify(response)), 400


service_view = ServiceView.as_view('service_view')
service_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/programs/<int:program_id>/services/',
    view_func=service_view, methods=['POST'])
