# services/ovpn_server/project/apit/cert_manage.py

import requests

from flask import current_app

from project.api.cert_gen import EasyRSA
from project.api.utils import file_check

from shutil import copy2


def create_req(file_name):
    """
    Creates the .req and .key files. Sends .key and .req to /usr/certs
    and uploads .req file to cert-server
    """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    if file_check(file_name + '.req'):
        response_object['status'] = 'success'
        response_object['message'] = file_name + '.req already exists'
        return response_object, 200
    req_resp = EasyRSA().req_gen(file_name)
    if 'Fail' in req_resp:
        response_object['message'] = req_resp
        return response_object, 400
    pki_path = current_app.config['PKI_PATH']
    req_path = current_app.config['REQ_PATH']
    copy2(pki_path + '/private/' + file_name + '.key', req_path)
    copy2(pki_path + '/reqs/' + file_name + '.req', req_path)
    url = current_app.config['CERT_SERVER_URL'] + '/cert/upload'
    content = (f'{file_name}.req', open(f'{req_path}/{file_name}.req'))
    headers = {'content_type': 'multipart/form-data'}
    files = {'file': content}
    resp = requests.post(url=url, files=files, headers=headers)
    return resp
