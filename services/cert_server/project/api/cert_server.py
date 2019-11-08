# services/cert_server/project/api/users.py

import os

from flask import Blueprint, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

from project.api.utils import file_check, allowed_file
from project.api.cert_manage import create_crt

cert_server_blueprint = Blueprint('cert-server', __name__)
api = Api(cert_server_blueprint)


class CertPing(Resource):
    def get(self):
        response_object = {
            'status': 'success',
            'message': 'pong!'
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
            if filename.split('.')[1] == 'req':
                return create_crt(filename)
            response_object['message'] = filename + ' file uploaded'
            return response_object, 200
        else:
            response_object['message'] = 'Not a valid file'
            return response_object, 400


api.add_resource(CertPing, '/cert/ping')
api.add_resource(Certificates, '/cert/upload')
