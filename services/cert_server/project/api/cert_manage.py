# services/cert_server/project/apit/cert_manage.py

import requests

from flask import current_app

from project.api.cert_gen import EasyRSA
from project.api.utils import file_check

from shutil import copy2


def create_ca():
    """
    Generates ca.crt and ca.key files and uploads ca.crt file
    to ovpn-server
    """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if file_check('ca.crt'):
        response_object['status'] = 'success'
        response_object['message'] = 'ca.crt file already exists'
        return response_object, 200
    ca_resp = EasyRSA().build_ca()
    if 'Fail' in ca_resp:
        response_object['message'] = ca_resp
        return response_object, 400
    pki_path = current_app.config['PKI_PATH']
    req_path = current_app.config['REQ_PATH']
    copy2(pki_path + '/ca.crt', req_path)
    copy2(pki_path + '/private/ca.key', req_path)
    url = current_app.config['OVPN_SERVER_URL'] + '/ovpn/certs'
    content = ('ca.crt', open(pki_path + '/ca.crt'), 'multipart/form-data')
    files = {'file': content}
    resp = requests.post(url=url, files=files)
    return resp.text, resp.status_code


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
    req_resp = EasyRSA().import_req(name)
    if 'Fail' in req_resp:
        response_object['message'] = f'Could not import {file_name}'
        response_object['detail'] = str(req_resp)
        return response_object, 400
    sign_resp = EasyRSA().sign_req(name)
    if 'Fail' in sign_resp:
        response_object['message'] = f'Could not generate {name}.crt'
    pki_path = current_app.config['PKI_PATH']
    req_path = current_app.config['REQ_PATH']
    copy2(pki_path + f'/issued/{name}.crt', req_path)
    url = current_app.config['OVPN_SERVER_URL'] + '/ovpn/certs'
    content = (f'{name}.crt', open(f'{req_path}/{name}.crt'))
    headers = {'content_type': 'multipart/form-data'}
    files = {'file': content}
    resp = requests.post(url=url, files=files, headers=headers)
    return resp.text, resp.status_code
