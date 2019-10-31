# services/cert_server/project/api/users.py


from flask import Blueprint
from flask_restful import Resource, Api

ovpn_server_blueprint = Blueprint('ovpn-server', __name__)
api = Api(ovpn_server_blueprint)


class OvpnPing(Resource):
    def get(self):
        response_object = {
            'status': 'success',
            'message': 'All men must serve'
        }
        return response_object, 200


api.add_resource(OvpnPing, '/ovpn/ping')
