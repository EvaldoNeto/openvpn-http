# services/cert_server/project/apit/cert_gen.py

import subprocess

from flask import current_app
from shutil import rmtree


class EasyRSA:

    def __init__(self):
        pass

    def init_pki(self):
        cmd = f'easyrsa --batch init-pki'
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return f'Failed to generate pki folder {str(e)}'
        return 'Success, pki folder created'

    def rm_pki(self):
        pki_path = current_app.config['PKI_PATH']
        rmtree(pki_path)

    def req_gen(self, filename):
        """
        Generates the requisition file with the name being the given file_name
        :param file_name: - :return: string
        """
        cmd = f'easyrsa --batch --req-cn={filename} gen-req {filename} nopass'
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to generate .req file for ' + filename + ' ' + \
                    str(e)
        return 'Success, .req file for ' + filename + ' created.'

    def import_req(self, file_name):
        cmd = f'easyrsa --batch import-req {file_name}.req'
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to import requisition ' + str(e)
        return 'Success, requisition imported'

    def build_ca(self):
        cmd = 'easyrsa --batch build-ca nopass'
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to build ca certificate ' + str(e)
        return 'Success, ca certificate created'

    def sign_req(self, file_name, is_server=False):
        """
        Generates the crt file with the name being the given file_name
        :param file_name: - :return: string
        """
        cmd = ''
        if is_server:
            cmd = f'easyrsa --batch sign-req server {file_name}'
        else:
            cmd = f'easyrsa --batch sign-req client {file_name}'
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to generate .crt file ' + str(e)
        return 'Success, .crt file generated for ' + file_name
