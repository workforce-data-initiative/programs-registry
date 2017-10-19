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






