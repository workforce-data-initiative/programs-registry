from flask import Blueprint, make_response, request, jsonify, abort
from flask.views import MethodView

from app.models import Location


location_blueprint = Blueprint('location', __name__)

class LocationView(MethodView):
    """
    This class handles API requests for the location resource.

    /api/organizations/<org_id>/locations/ - GET
    /api/organizations/<org_id>/locations -POST
     /api/organizations/<org_id>/locations/<id> - PUT
    /api/organizations/<org_id>/locations/<id> - DELETE
    """

    def post(self, organization_id):
        """
        Create a location and return it as json.
        """
        try:
            payload = request.data.to_dict()
            if organization_id is not None:
                payload['organization_id'] = organization_id
                location = Location(**payload)
                location.save()
                response = location.serialize()
                return make_response(jsonify(response)), 201
            else:
                abort(404)

        except Exception as e:
            response = { "message": str(e) }
            return make_response(jsonify(response)), 400


    def get(self, organization_id, location_id):
        """
        Get an existing locations(s) and return as json response.
        """
        if location_id is not None:
            # handle get by id
            try:
                location = Location.query.filter_by(id=location_id).first()
                response = location.serialize()
                return make_response(jsonify(response)), 200

            except Exception as e:
                response = { "message": str(e) }
                return make_response(jsonify(response)), 400
        else:
            # handle get all
            locations = Location.get_all(organization_id)
            response = []

            for location in locations:
                response.append(location.serialize())
            return make_response(jsonify(response)), 200

    def put(self, organization_id, location_id):
        """
        Update an existing location and return a json response of it."""

        if location_id is not None:
            try:
                location = Location.query.filter_by(id=location_id).first()

                for key in request.data.to_dict().keys():
                    setattr(location, key, request.data.get(key))
                location.save()
                response = location.serialize()
                return make_response(jsonify(response)), 200

            except Exception as e:
                response = {"message": str(e) }
                return make_response(jsonify(response)), 400
        else:
            abort(404)

    def delete(self, organization_id, location_id):
        """Delete a location given its id."""

        if location_id is not None:
            try:
                location = Location.query.filter_by(id=location_id).first()
                location.delete()
                res = location.serialize()
                return make_response(jsonify(res)), 202

            except Exception as e:
                res = { "message": str(e) }
                return make_response(jsonify(res)), 400


location_view = LocationView.as_view('location_view')
location_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/locations/',
    view_func=location_view,
    methods=['POST'])
location_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/locations/',
    view_func=location_view, defaults={'location_id': None},
    methods=['GET'])
location_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/locations/<int:location_id>',
    view_func=location_view,
    methods=['GET', 'POST', 'DELETE'])


