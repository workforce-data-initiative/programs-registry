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
            if request.headers['Content-Type'] == "application/json":
                payload = request.data
            elif request.form:
                payload = request.data.to_dict()
            else:
                payload = request.get_json(force=True)

            if organization_id is not None:
                payload['organization_id'] = organization_id
                location = Location(**payload)
                location.save()
                response = location.serialize()
                return make_response(jsonify(response)), 201
            else:
                abort(404)

        except Exception as e:
            response = {"message": str(e)}
            return make_response(jsonify(response)), 400

    def get(self, organization_id, location_id):
        """
        Get an existing locations(s) and return as json response.
        """
        if location_id is not None:
            # handle get by id
            location = Location.query.filter_by(id=location_id).first()
            if not location:
                abort(404)
            else:
                try:
                    response = location.serialize()
                    return make_response(jsonify(response)), 200

                except Exception as e:
                    response = {"message": str(e)}
                    return make_response(jsonify(response)), 400
        else:
            # handle get all
            locations = Location.get_all(organization_id)
            response = []

            if request.args.get('name'):
                # search by name
                location_name = request.args.get('name')
                results = db.session.query(Location).filter(
                    Location.name.ilike('%{0}%'.format(location_name)))
                locations = results

            for location in locations:
                response.append(location.serialize())
            return make_response(jsonify(response)), 200

    def put(self, organization_id, location_id):
        """
        Update an existing location and return a json response of it."""
        if request.headers['Content-Type'] == "application/json":
            payload = request.data
        elif request.form:
            payload = request.data.to_dict()
        else:
            payload = request.get_json(force=True)

        if location_id is not None:
            try:
                location = Location.query.filter_by(id=location_id).first()

                for key in payload.keys():
                    setattr(location, key, request.data.get(key))
                location.save()
                response = location.serialize()
                return make_response(jsonify(response)), 200

            except Exception as e:
                response = {"message": str(e)}
                return make_response(jsonify(response)), 400
        else:
            abort(404)

    def delete(self, organization_id, location_id):
        """Delete a location given its id."""

        if location_id is not None:
            location = Location.query.filter_by(id=location_id).first()
            if not location:
                abort(404)
            else:
                try:
                    location.delete()
                    return make_response(jsonify({})), 202

                except Exception as e:
                    res = {"message": str(e)}
                    return make_response(jsonify(res)), 400
        else:
            abort(404)


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
    methods=['GET', 'PUT', 'DELETE'])
