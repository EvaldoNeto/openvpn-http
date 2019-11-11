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

    def gen_dh(self):
        cmd = 'easyrsa --batch gen-dh'
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to generate Diffie-Hellman certificate ' + str(e)
        return 'Success, Diffie-Hellman certificate generated'

    def sign_req(self, file_name):
        """
        Generates the crt file with the name being the given file_name
        :param file_name: - :return: string
        """
        cmd = f'easyrsa --batch sign-req client {file_name}'
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to generate .crt file ' + str(e)
        return 'Success, .crt file generated for ' + file_name

    def ovpn_gen(self, crt_path, key_path, ca_path):
        """
        Generates the .ovpn file based on the ,crt and .key files
        :param crt_path: the full path to the .crt file
        :param key_path: the full path to the .key file
        :param ca_path: the full path to the ca.crt file
        """
        crt_file = open(crt_path)
        key_file = open(key_path)
        ca_file = open(ca_path)
        base_conf_file = open('/usr/src/app/base.conf')
        ovpn_content = base_conf_file.read() + '<ca>\n' + ca_file.read()
        ovpn_content = ovpn_content + '</ca>\n<cert>\n' + crt_file.read()
        ovpn_content = ovpn_content + '</cert>\n<key>\n' + key_file.read()
        ovpn_content = ovpn_content + '</key>\n'
        file_name = crt_path.split('/')[len(crt_path.split('/')) - 1]
        file_name = file_name.split('.')[0]
        output = open(f'/usr/share/certs/ovpn/{file_name}.ovpn', 'w')
        output.write(ovpn_content)

    def revoke(self, filename):
        cmd = f'easyrsa --batch revoke {filename}'
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return f'Failed to revoke {filename}.crt {str(e)}'
        return f'Success, {filename}.crt revoked'
