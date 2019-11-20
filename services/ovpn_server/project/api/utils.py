# services/ovpn_server/project/apit/cert_manage.py

import os

from flask import current_app, request

from functools import wraps


def allowed_file(file_name):
    ext = set(['ovpn', 'crt'])
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ext


def file_check(filename):
    """
    Checks if the certificate file already exists
    THe file_name must contain the extension
    """
    pki_path = current_app.config['PKI_PATH']
    return os.path.isfile(f'{pki_path}/reqs/{filename}') and \
        allowed_file(filename)


def authenticate_restful(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return response_object, 403
        auth_token = auth_header.split(' ')[1]
        if auth_token != current_app.config['SECRET_KEY']:
            return response_object, 401
        response_object['status'] = 'success'
        response_object['message'] = 'Valid auth token provided'
        return f(response_object, *args, **kwargs)
    return decorated_function
