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

    def get(self, organization_id, program_id, service_id):
        """Get a service and return it as json."""

        if service_id is not None:
            # handle the get by id
            try:
                service = Service.query.filter_by(id=service_id).first()
                response = service.serialize()
                return make_response(jsonify(response)), 200

            except Exception as e:
                response = { "message": str(e) }
                return make_response(jsonify(response)), 400
        else:
            # handle get all
            try:
                services = Service.get_all(organization_id)
                response = []

                for service in services:
                    response.append(service.serialize())
                return make_response(jsonify(response)), 200
            except Exception as e:
                response = {"message": str(e)}
                return make_response(jsonify(e)), 400

    def put(self, organization_id, program_id, service_id):
        """Update a service and return it as json."""

        if service_id is not None:
            try:
                service = Service.query.filter_by(id=service_id).first()
                for key in request.data.to_dict().keys():
                    setattr(service, key, request.data.get(key))

                service.save()
                response = service.serialize()
                return make_response(jsonify(response)), 200

            except Exception as e:
                response = { "message": str(e) }
                return make_response(jsonify(response)), 400
        else:
            abort(404)

    def delete(self, organization_id, program_id, service_id):
        """Delete a program given its id."""

        if service_id is not None:
            try:
                service = Service.query.filter_by(id=service_id).first()
                service.delete()

                return make_response(jsonify({})), 202

            except Exception as e:
                response = { "message": str(e) }
                return make_response(jsonify(response)), 400
        else:
            abort(404)



service_view = ServiceView.as_view('service_view')
service_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/programs/<int:program_id>/services/',
    view_func=service_view, methods=['POST'])
service_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/programs/<int:program_id>/services/',
    view_func=service_view, defaults={'service_id': None}, methods=['GET'])
service_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/programs/<int:program_id>/services/<int:service_id>',
    view_func=service_view, methods=['GET', 'PUT', 'DELETE'])

