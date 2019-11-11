# services/cert_server/project/api/users.py

from flask import Blueprint, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

from project.api.utils import allowed_file
from project.api.cert_manage import create_crt, save_file

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
        cert_gen = True
        if request.form.get('cert') == 'False':
            cert_gen = False
        if file.filename == '':
            response_object['message'] = 'No file selected for upload'
            return response_object, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            resp, stat = save_file(file)
            if stat != 200:
                return resp, stat
            if filename.split('.')[1] == 'req' and cert_gen:
                return create_crt(filename)
            response_object['status'] = 'success'
            response_object['message'] = filename + ' file uploaded'
            return response_object, 200
        else:
            response_object['message'] = 'Not a valid file'
            return response_object, 400


api.add_resource(CertPing, '/cert/ping')
api.add_resource(Certificates, '/cert/upload')
