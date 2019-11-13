# services/ovpn_server/project/apit/cert_manage.py

import requests
import os

from flask import current_app

from project.api.cert_gen import EasyRSA
from project.api.utils import file_check

from werkzeug.utils import secure_filename


def create_req(file_name):
    """
    Creates the .req and .key files. Sends .key and .req to /usr/certs
    and uploads .req file to cert-server
    """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    if len(file_name.split('.')) != 1:
        return response_object, 400
    if file_check(file_name + '.req'):
        response_object['status'] = 'success'
        response_object['message'] = file_name + '.req already exists'
        return response_object, 200
    req_resp = EasyRSA().req_gen(file_name)
    if 'Fail' in req_resp:
        response_object['message'] = req_resp
        return response_object, 400
    pki_path = current_app.config['PKI_PATH']
    url = current_app.config['CERT_SERVER_URL'] + '/cert/upload'
    content = (f'{file_name}.req', open(f'{pki_path}/reqs/{file_name}.req'))
    headers = {'content_type': 'multipart/form-data'}
    files = {'file': content}
    resp = requests.post(url=url, files=files, headers=headers)
    return resp.text, resp.status_code


def check_pki():
    pki_path = current_app.config['PKI_PATH']
    return os.path.isdir(pki_path)


def save_file(file):
    filename = secure_filename(file.filename)
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    if not check_pki():
        response_object['message'] = 'pki folder does not exist,' + \
            ' please initiate it'
        return response_object, 400
    if file_check(filename):
        response_object['message'] = filename + ' file already exists'
        return response_object, 400
    paths = {
        'ovpn': current_app.config['OVPN_CERTS_PATH'],
        'crt': current_app.config['CRT_CERTS_PATH'],
        'ca': current_app.config['OPENVPN']
    }
    file.save(os.path.join(paths[filename.split('.')[1]], filename))
    if filename == 'ca.crt':
        paths['ca']
    else:
        paths[filename.split('.')[1]]
    response_object['status'] = 'success'
    response_object['message'] = f'File {filename} saved'
    return response_object, 200
