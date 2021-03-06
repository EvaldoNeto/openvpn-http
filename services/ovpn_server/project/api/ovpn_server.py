# services/cert_server/project/api/users.py

from flask import Blueprint, request, current_app, send_file
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

from project.api.utils import allowed_file, authenticate_restful
from project.api.cert_manage import create_req, save_file, initiate_ovpn,\
    generate_ovpn_file, transfer_req

ovpn_server_blueprint = Blueprint('ovpn-server', __name__)
api = Api(ovpn_server_blueprint)


class OvpnFile(Resource):

    method_decorators = {'get': [authenticate_restful]}

    def get(self, resp, filename):
        ovpn_files_path = current_app.config['OVPN_CERTS_PATH']
        response_object = {
            'status': 'fail',
            'message': f'{filename} file not found'
        }
        try:
            return send_file(f'{ovpn_files_path}/{filename}')
        except Exception:
            return response_object, 401


class OvpnPing(Resource):

    def get(self):
        response_object = {
            'status': 'success',
            'message': 'All men must serve'
        }
        return response_object, 200


class Certificates(Resource):

    method_decorators = {'post': [authenticate_restful]}

    def post(self, resp):
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
            response, stat = save_file(file)
            if stat != 200:
                return response, stat
            if filename == 'ca.crt':
                response_object['status'] = 'success'
                response_object['message'] = 'ca.crt uploaded to ovpn-server'
                return response_object, 200
            if filename == 'server.crt':
                return initiate_ovpn()
            elif '.crt' in filename and 'test' not in filename:
                return generate_ovpn_file(filename.split('.')[0])
            return response, stat
        else:
            response_object['message'] = 'Not a valid file'
            return response_object, 400


class CreateReq(Resource):

    method_decorators = {'post': [authenticate_restful]}

    def post(self, resp):
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        post_data = request.get_json()
        if not post_data:
            response_object['message'] = 'CreateReq Invalid payload'
            return response_object, 400
        certname = post_data.get('certname')
        return create_req(certname)


class TransferReq(Resource):

    method_decorators = {'post': [authenticate_restful]}

    def post(self, resp):
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        post_data = request.get_json()
        if not post_data:
            response_object['message'] = 'TransferReq Invalid payload'
            return response_object, 400
        certname = post_data.get('certname')
        return transfer_req(certname)


api.add_resource(OvpnPing, '/ovpn/ping')
api.add_resource(Certificates, '/ovpn/certs')
api.add_resource(CreateReq, '/ovpn/create_req')
api.add_resource(TransferReq, '/ovpn/transfer_req')
api.add_resource(OvpnFile, '/ovpn/file/<filename>')
