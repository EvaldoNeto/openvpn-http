# services/cert_server/project/apit/cert_manage.py

import requests
import os

from flask import current_app
from werkzeug.utils import secure_filename

from project.api.cert_gen import EasyRSA
from project.api.utils import file_check


def create_crt(file_name):
    """
    Generates .crt files from .req files coming from ovpn-server
    and send the .crt files to ovpn-server
    """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    name, ext = file_name.split('.')
    if ext != 'req':
        return response_object, 400
    pki_path = current_app.config['PKI_PATH']
    if not os.path.isfile(f'{pki_path}/reqs/{file_name}'):
        response_object['message'] = f'File {file_name} not found'
        return response_object, 400
    sign_resp = EasyRSA().sign_req(name)
    if 'Fail' in sign_resp:
        response_object['message'] = f'Could not generate {name}.crt'
        return response_object, 400
    response_object['status'] = 'success'
    response_object['message'] = f'{file_name} created on cert-server'
    return response_object, 200


def transfer_crt(filename):
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    pki_path = current_app.config['PKI_PATH']
    if not os.path.isfile(f'{pki_path}/issued/{filename}.crt'):
        response_object['message'] = f'{filename}.crt does not exists'
        return response_object, 400
    url = current_app.config['OVPN_SERVER_URL'] + '/ovpn/certs'
    content = (f'{filename}.crt', open(f'{pki_path}/issued/{filename}.crt'))
    headers = {'content_type': 'multipart/form-data'}
    files = {'file': content}
    resp = requests.post(url=url, files=files, headers=headers)
    return resp.text, resp.status_code


def check_pki():
    pki_path = current_app.config['PKI_PATH']
    return os.path.isdir(pki_path)


def check_ca():
    pki_path = current_app.config['PKI_PATH']
    return os.path.isfile(f'{pki_path}/ca.crt') and \
        os.path.isfile(f'{pki_path}/private/ca.key')


def save_file(file):
    filename = secure_filename(file.filename)
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    pki_path = current_app.config['PKI_PATH']
    if not check_pki():
        response_object['message'] = 'pki folder does not exist,' + \
            ' please initiate it'
        return response_object, 400
    if file_check(filename):
        response_object['message'] = filename + ' file already exists'
        return response_object, 400
    paths = {
        'req': f'{pki_path}/reqs'
    }
    file.save(os.path.join(paths[filename.split('.')[1]], filename))
    paths[filename.split('.')[1]]
    response_object['status'] = 'success'
    response_object['message'] = f'File {filename} saved'
    return response_object, 200


def create_ca():
    """
    Generates ca.crt and ca.key files and uploads ca.crt file
    to ovpn-server
    """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    pki_path = current_app.config['PKI_PATH']
    if not check_pki():
        response_object['message'] = 'pki folder does not exist,' + \
            ' please initiate it'
        return response_object, 400
    if check_ca():
        return 'ca file already exists'
    resp = EasyRSA().build_ca()
    if 'Fail' in resp:
        response_object['message'] = resp
        return response_object, 400
    if not check_ca():
        response_object['message'] = 'Missing ca.key or ca.crt'
        return response_object, 400
    url = current_app.config['OVPN_SERVER_URL'] + '/ovpn/certs'
    content = (f'ca.crt', open(f'{pki_path}/ca.crt'))
    headers = {'content_type': 'multipart/form-data'}
    files = {'file': content}
    resp = requests.post(url=url, files=files, headers=headers)
    return resp.text, resp.status_code
