# services/ovpn_server/project/apit/cert_manage.py

import requests
import os

from flask import current_app
from werkzeug.utils import secure_filename

from project.api.cert_gen import EasyRSA
from project.api.utils import file_check

from shutil import copy2


def create_req(file_name):
    """
    Creates the .req and .key files
    """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    if len(file_name.split('.')) != 1:
        return response_object, 400
    pki_path = current_app.config['PKI_PATH']
    if os.path.isfile(f'{pki_path}/reqs/{file_name}.crt'):
        response_object['status'] = 'fail'
        response_object['message'] = file_name + '.req already exists'
        return response_object, 200
    req_resp = EasyRSA().req_gen(file_name)
    if 'Fail' in req_resp:
        response_object['message'] = req_resp
        return response_object, 400
    response_object['status'] = 'success'
    response_object['message'] = f'{file_name} created on ovpn-server'
    return response_object, 200


def transfer_req(filename):
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    if len(filename.split('.')) != 1:
        response_object['message'] = 'transfer_req Invalid payload'
        return response_object, 400
    pki_path = current_app.config['PKI_PATH']
    if not os.path.isfile(f'{pki_path}/reqs/{filename}.req'):
        response_object['message'] = f'{filename}.req does not exist'
        return response_object, 400
    pki_path = current_app.config['PKI_PATH']
    url = current_app.config['CERT_SERVER_URL'] + '/cert/upload'
    content = (f'{filename}.req', open(f'{pki_path}/reqs/{filename}.req'))
    headers = {'content_type': 'multipart/form-data'}
    files = {'file': content}
    resp = requests.post(url=url, files=files, headers=headers)
    return resp.text, resp.status_code


def check_pki():
    pki_path = current_app.config['PKI_PATH']
    return os.path.isdir(pki_path)


def initiate_ovpn():
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    crt_path = current_app.config['CRT_CERTS_PATH']
    openvpn_path = current_app.config['OPENVPN']
    pki_path = current_app.config['PKI_PATH']
    copy2(f'{crt_path}/ca.crt', openvpn_path)
    copy2(f'{crt_path}/server.crt', openvpn_path)
    if not check_pki():
        response_object['message'] = 'pki folder does not exist,' + \
            ' please initiate it'
        return response_object, 400
    EasyRSA().gen_dh()
    copy2(f'{pki_path}/dh.pem', openvpn_path)
    copy2(f'{pki_path}/private/server.key', openvpn_path)
    response_object['status'] = 'success'
    response_object['message'] = 'ovpn configured'
    return response_object, 200


def generate_ovpn_file(filename):
    crt_path = f'{current_app.config["CRT_CERTS_PATH"]}/{filename}.crt'
    key_path = f'{current_app.config["PKI_PATH"]}/private/{filename}.key'
    ca_path = f'{current_app.config["OPENVPN"]}/ca.crt'
    EasyRSA().ovpn_gen(crt_path, key_path, ca_path)
    ovpn_path = current_app.config['OVPN_CERTS_PATH']
    response_object = {
        'status': 'fail',
        'message': f'Could not create {filename}'
    }
    if os.path.isfile(f'{ovpn_path}/{filename}.ovpn'):
        response_object['status'] = 'success'
        response_object['message'] = f'{filename} created'
        return response_object, 200
    return response_object, 400


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
        'crt': current_app.config['CRT_CERTS_PATH']
    }
    file.save(os.path.join(paths[filename.split('.')[1]], filename))
    response_object['status'] = 'success'
    response_object['message'] = f'File {filename} saved'
    return response_object, 200


def create_server():
    crt_path = current_app.config["CRT_CERTS_PATH"]
    if not os.path.isfile(f'{crt_path}/ca.crt'):
        return 'Missing ca.crt, please create it with docker-compose' +\
            'exec cert-server python manage.py create_ca'
    resp, stat = create_req('server')
    if stat != 200:
        return resp, stat
    return transfer_req('server')
