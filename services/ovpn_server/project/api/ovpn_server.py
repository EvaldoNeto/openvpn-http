# services/cert_server/project/api/users.py

import os

from flask import Blueprint, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

from project.api.utils import file_check, allowed_file
from project.api.cert_manage import create_req

ovpn_server_blueprint = Blueprint('ovpn-server', __name__)
api = Api(ovpn_server_blueprint)


class OvpnPing(Resource):
    def get(self):
        response_object = {
            'status': 'success',
            'message': 'All men must serve'
        }
        return response_object, 200


class Certificates(Resource):
    def post(self):
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        if 'file' not in request.files:
            response_object['message'] = 'No file part'
            return response_object, 400
        file = request.files['file']
        if file.filename == '':
            response_object['message'] = 'No file selected for upload'
            return response_object, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            response_object['status'] = 'success'
            if file_check(filename):
                response_object['message'] = filename + ' file already exists'
                return response_object, 200
            file.save(os.path.join(os.environ.get('REQ_PATH'), filename))
            response_object['message'] = filename + ' file uploaded'
            return response_object, 200
        else:
            response_object['message'] = 'Not a valid file'
            return response_object, 400


class CreateCert(Resource):
    def post(self):
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        post_data = request.get_json()
        if not post_data:
            return response_object, 400
        certname = post_data.get('certname')
        return create_req(certname)


api.add_resource(OvpnPing, '/ovpn/ping')
api.add_resource(Certificates, '/ovpn/certs')
api.add_resource(CreateCert, '/ovpn/create_crt')
