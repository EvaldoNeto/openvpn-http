# services/cert_server/project/apit/cert_manage.py

import os

from flask import current_app


def allowed_file(file_name):
    ext = set(['req'])
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ext


def file_check(filename):
    """
    Checks if the certificate file already exists
    THe file_name must contain the extension
    """
    pki_path = current_app.config['PKI_PATH']
    return os.path.isfile(f'{pki_path}/reqs/{filename}') and \
        allowed_file(filename)
