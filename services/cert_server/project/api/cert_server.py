# services/cert_server/project/api/users.py

import os

from flask import Blueprint, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

from project.api.cert_gen import EasyRSA

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
    """
    Upload method based on the following tutorial
    https://www.roytuts.com/python-flask-file-upload-example/
    """
    ALLOWED_EXTENSIONS = set(['req', 'ovpn'])

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() \
            in self.ALLOWED_EXTENSIONS

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
            response_object['message'] = 'No file selected to upload'
            return response_object, 400
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('/usr/certs', filename))
            mopa = EasyRSA().cert_gen(filename.rsplit('.')[0])
            response_object['message'] = 'File successfully uploaded.'
            response_object['message'] = mopa
            response_object['status'] = 'success'
            return response_object, 200
        else:
            response_object['message'] = 'Only .req files allowed'
            return response_object, 401

    def get(self):
        response_object = {
            'status': 'success',
            'message': 'Oh yeah!'
        }
        return response_object, 200


api.add_resource(CertPing, '/cert/ping')
api.add_resource(Certificates, '/cert/upload')
