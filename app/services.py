from flask import Blueprint, make_response, request, jsonify, abort
from flask.views import MethodView

from app.models import Service, Organization, Program


service_blueprint = Blueprint('service', __name__)


class ServiceView(MethodView):
    """
    This class handles api requests for the service resource.

    Accepted endpoints include:
    /api/organizations/<org_id>/programs/<program_id>/services/ - GET
    /api/organizations/<org_id>/programs/<program_id>/services/ - POST
    /api/organizations/<org_id>/services/ - POST
    /api/organizations/<org_id>/programs/<program_id>/services/<id> - PUT
    /api/organizations/<org_id>/programs/<program_id>/services/<id> - DELETE
    """

    def post(self, organization_id, program_id):
        """
        Create a service and return a json response containing it.
        """
        if request.headers['Content-Type'] == "application/json":
            payload = request.data
        elif request.form:
            payload = request.data.to_dict()
        else:
            payload = request.get_json(force=True)

        # validation check for org
        org = Organization.query.filter_by(id=organization_id).first()
        if not org:
            abort(404)

        # First, check to see whether the service comes under a given program
        if program_id is not None:
            try:
                # check whether the program exists
                prog = Program.query.filter_by(id=program_id).first()
                abort(404) if prog is None else prog

                if organization_id is not None:
                    # check to see whether the org exists
                    org = Organization.query.filter_by(
                        id=organization_id).first()
                    if org is not None:
                        payload['organization_id'] = organization_id
                        service = Service(**payload)
                        service.save()
                        response = service.serialize()
                        return make_response(jsonify(response)), 201
                    else:
                        # the org is none-existent - return 404 not found
                        abort(404)
            except Exception as e:
                response = {"message": str(e)}
                return make_response(jsonify(response)), 400
        else:
            # Create the service without the program ID (the service is on its
            # own
            if organization_id is not None:
                org = Organization.query.filter_by(
                    id=organization_id).first()
                if org is not None:
                    payload['organization_id'] = organization_id
                    service = Service(**payload)
                    service.save()
                    response = service.serialize()
                    return make_response(jsonify(response)), 201
                else:
                    # the org doe not exist
                    abort(404)
            else:
                abort(404)

    def get(self, organization_id, program_id, service_id):
        """Get a service and return it as json."""

        org = Organization.query.filter_by(id=organization_id).first()
        if not org:
            abort(404)

        service = Service.query.filter_by(id=service_id).first()
        if service_id is not None:
            if program_id is None:
                # handle get by id for a service that is not under any program
                if not service:
                    abort(404)
                else:
                    response = service.serialize()
                    return make_response(jsonify(response)), 200

            else:
                # handle the get by id for service under a program
                program = Program.query.filter_by(id=program_id).first()
                if not program:
                    abort(404)
                else:
                    if not service:
                        abort(404)
                    if service.program_id != program_id:
                        abort(404)
                    else:
                        try:
                            response = service.serialize()
                            return make_response(jsonify(response)), 200
                        except Exception as e:
                            response = {"message": str(e)}
                            return make_response(jsonify(response)), 400
        else:
            # handle get all
            try:
                services = Service.get_all(organization_id)
                response = []

                if request.args.get('name'):
                    name = request.args.get('name')
                    search = services.filter(
                        Service.name.ilike('%{0}%'.format(name)))
                    if search is None:
                        abort(404)
                    services = search

                for service in services:
                    response.append(service.serialize())
                return make_response(jsonify(response)), 200
            except Exception as e:
                response = {"message": str(e)}
                return make_response(jsonify(e)), 400

    def put(self, organization_id, program_id, service_id):
        """Update a service and return it as json."""

        if service_id is not None:
            # test that the org exists
            org = Organization.query.filter_by(id=organization_id).first()
            service = Service.query.filter_by(id=service_id).first()
            if org is None:
                abort(404)
            if service is None:
                abort(404)

            try:
                if request.headers['Content-Type'] == "application/json":
                    payload = request.data
                elif request.form:
                    payload = request.data.to_dict()
                else:
                    payload = request.get_json(force=True)

                for key in payload.keys():
                    setattr(service, key, payload.get(key))

                service.save()
                response = service.serialize()
                return make_response(jsonify(response)), 200

            except Exception as e:
                response = {"message": str(e)}
                return make_response(jsonify(response)), 400
        else:
            abort(404)

    def delete(self, organization_id, program_id, service_id):
        """Delete a program given its id."""

        org = Organization.query.filter_by(id=organization_id).first()
        if not org:
            abort(404)

        if program_id is None and service_id is not None:
            # the service has no program associated to it
            try:
                service = Service.query.filter_by(id=service_id).first()
                service.delete()
                return make_response(jsonify({})), 202
            except Exception as e:
                response = {"message": str(e)}
                return make_response(jsonify(response)), 400

        if service_id is not None:
            try:
                service = Service.query.filter_by(id=service_id).first()
                service.delete()

                return make_response(jsonify({})), 202

            except Exception as e:
                response = {"message": str(e)}
                return make_response(jsonify(response)), 400
        else:
            abort(404)


service_view = ServiceView.as_view('service_view')
service_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/services/',
    view_func=service_view, defaults={'program_id': None}, methods=['POST'])
service_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/services/<int:service_id>',
    view_func=service_view, defaults={'program_id': None},
    methods=['GET', 'PUT', 'DELETE'])
service_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/programs/' +
    '<int:program_id>/services/',
    view_func=service_view, methods=['POST'])
service_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/programs/' +
    '<int:program_id>/services/',
    view_func=service_view, defaults={'service_id': None}, methods=['GET'])
service_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/programs/' +
    '<int:program_id>/services/<int:service_id>',
    view_func=service_view, methods=['GET', 'PUT', 'DELETE'])
