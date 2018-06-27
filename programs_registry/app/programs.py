from flask import Blueprint, make_response, request, jsonify, abort
from flask.views import MethodView

from app.models import db, Program, Organization


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

        org = Organization.query.filter_by(id=organization_id).first()
        if not org:
            abort(404)
        else:
            try:
                if request.headers['Content-Type'] == "application/json":
                    payload = request.get_json(silent=True)
                elif request.form:
                    payload = request.data.to_dict()
                else:
                    payload = request.get_json(force=True)

                payload['organization_id'] = organization_id
                program = Program(**payload)
                program.save()
                response = program.serialize()
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {"message": str(e)}
                return make_response(jsonify(response)), 400

    def get(self, organization_id, program_id):
        """
        Get an existing program(s) and return as a json response
        """

        org = Organization.query.filter_by(id=organization_id).first()
        if not org:
            abort(404)

        if program_id is not None:
            # handle the get by id
            program = Program.query.filter_by(id=program_id).first()
            if not program:
                abort(404)
            else:
                try:
                    response = program.serialize()
                    return make_response(jsonify(response)), 200

                except Exception as e:
                    response = {"message": str(e)}
                    return make_response(jsonify(response)), 400
        else:
            # handle get all
            programs = Program.query.filter_by(organization_id=organization_id)

            if request.args.get('name'):
                # Search by name
                search_query = request.args.get('name')
                search_results = db.session.query(Program).filter(
                    Program.name.ilike('%{0}%'.format(search_query)))
                programs = search_results
            response = [prog.serialize() for prog in programs]

            return make_response(jsonify(response)), 200

    def put(self, organization_id, program_id):
        """Update an existing program and return a json response."""

        org = Organization.query.filter_by(id=organization_id).first()
        if not org:
            abort(404)

        if program_id is not None:
            try:
                response = {}
                program = Program.query.filter_by(id=program_id).first()

                if request.headers['Content-Type'] == "application/json":
                    payload = request.data
                elif request.form:
                    payload = request.data.to_dict()
                else:
                    payload = request.get_json(force=True)

                for key in payload.keys():
                    setattr(program, key, payload.get(key))

                program.save()
                response = program.serialize()
                return make_response(jsonify(response)), 200

            except Exception as e:
                if not program:
                    abort(404)
                response = {"message": str(e)}
                return make_response(jsonify(response)), 400
        else:
            abort(404)

    def delete(self, organization_id, program_id):
        """Delete a program given its id."""

        org = Organization.query.filter_by(id=organization_id).first()
        if not org:
            abort(404)

        if program_id is not None:
            prog = Program.query.filter_by(id=program_id).first()
            if not prog:
                abort(404)
            else:
                try:
                    prog.delete()
                    return make_response(jsonify({})), 202

                except Exception as e:
                    response = {"message": str(e)}
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
