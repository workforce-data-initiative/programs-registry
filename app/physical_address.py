from flask import Blueprint, make_response, request, jsonify, abort
from flask.views import MethodView

from app.models import PhysicalAddress, Organization, Location

address_blueprint = Blueprint('address', __name__)


class PhysicalAddressView(MethodView):
    """
    This class handles API requests for the physical address resource.

    /api/organizations/<org_id>/locations/<location_id>/addresses/ - GET
    /api/organizations/<org_id>/locations/<location_id>/addresses/ - POST
    /api/organizations/<org_id>/locations/<location_id>/addresses/<id> - PUT
    /api/organizations/<org_id>/locations/<location_id>/addresses/<id> - DELETE
    """

    def post(self, organization_id, location_id):
        """Create an address and return a json response of it."""

        try:
            if request.headers['Content-Type'] == "application/json":
                payload = request.data
            elif request.form:
                payload = request.data.to_dict()
            else:
                payload = request.get_json(force=True)

            if organization_id is not None:
                org = Organization.query.filter_by(id=organization_id).first()
                if not org:
                    abort(404)
                else:
                    if location_id is not None:
                        payload['location_id'] = location_id
                        address = PhysicalAddress(**payload)
                        address.save()
                        response = address.serialize()
                        return make_response(jsonify(response)), 201
                    else:
                        abort(404)
        except Exception as e:
            response = { "message": str(e) }
            return make_response(jsonify(response)), 400

    def get(self, organization_id, location_id, address_id):
        """Retrieve an address, returning it as json."""

        org = Organization.query.filter_by(id=organization_id).first()
        if not org:
            abort(404)
        else:
            loc = Location.query.filter_by(id=location_id).first()
            if not loc:
                abort(404)
        if address_id is not None:
            # get the address by id
            address = PhysicalAddress.query.filter_by(id=address_id).first()
            if not address:
                abort(404)
            else:
                try:
                    res = address.serialize()
                    return make_response(jsonify(res)), 200
                except Exception as e:
                    res = { "message": str(e) }
                    return make_response(jsonify(res)), 400
        else:
            # get all addresses
            addresses = PhysicalAddress.get_all(location_id)
            res = [address.serialize() for address in addresses]
            return make_response(jsonify(res)), 200


    def put(self, organization_id, location_id, address_id):
        """Update an address and return it as json."""

        if request.headers['Content-Type'] == "application/json":
            payload = request.data
        elif request.form:
            payload = request.data.to_dict()
        else:
            payload = request.get_json(force=True)

        org = Organization.query.filter_by(id=organization_id).first()
        if not org:
            abort(404)
        else:
            loc = Location.query.filter_by(id=location_id).first()
            if not loc:
                abort(404)

        if address_id is not None:
            try:
                address = PhysicalAddress.query.filter_by(
                    id=address_id).first()

                for key in payload.keys():
                    setattr(address, key, request.data.get(key))
                address.save()
                res = address.serialize()
                return make_response(jsonify(res)), 200
            except Exception as e:
                res = { "message": str(e) }
                return make_response(jsonify(res)), 400
        else:
            abort(404)

    def delete(self, organization_id, location_id, address_id):
        """Delete an address given its id."""

        org = Organization.query.filter_by(id=organization_id).first()
        if not org:
            abort(404)
        else:
            loc = Location.query.filter_by(id=location_id).first()
            if not loc:
                abort(404)

        if address_id is not None:
            address = PhysicalAddress.query.filter_by(id=address_id).first()
            if not address:
                abort(404)
            else:
                try:
                    address.delete()
                    return make_response(jsonify({})), 202
                except Exception as e:
                    res = { "message": str(e) }
                    return make_response(jsonify(res)), 500
        else:
            abort(404)


address_view = PhysicalAddressView.as_view('address_view')
address_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/locations/<int:location_id>/addresses/',
    view_func=address_view, methods=['POST'])
address_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/locations/<int:location_id>/addresses/',
    view_func=address_view, defaults={'address_id': None},
    methods=['GET'])
address_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>/locations/<int:location_id>/addresses/<int:address_id>',
    view_func=address_view,
    methods=['GET', 'PUT', 'DELETE'])


