# services/cert_server/project/apit/cert_manage.py

import os


def allowed_file(file_name):
    ext = set(['req', 'ovpn', 'crt'])
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ext


def file_check(filename):
    """
    Checks if the certificate file already exists
    THe file_name must contain the extension
    """
    req_path = os.environ.get('REQ_PATH')
    return os.path.isfile(req_path + '/' + filename) and allowed_file(filename)
