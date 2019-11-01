# services/cert_server/project/apit/cert_gen.py

import subprocess
import os


class EasyRSA:
    req_path = os.environ.get('REQ_PATH')

    def __init__(self):
        pass

    def req_gen(self, file_name):
        """
        Generates the requisition file with the name being the given file_name
        :param file_name: - :return: string
        """
        cmd = 'easyrsa --batch gen-req ' + file_name + ' nopass'
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to generate .req file for ' + file_name + ' ' + \
                    str(e)
        return 'Success, .req file for ' + file_name + ' created.'

    def import_req(self, file_name):
        cmd = 'easyrsa --batch import-req ' + self.req_path + '/' + \
              file_name + '.req ' + file_name
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to import requisition ' + str(e)
        return 'Success, requisition imported'

    def cert_gen(self, file_name):
        """
        Generates the crt file with the name being the given file_name
        :param file_name: - :return: string
        """
        cmd = 'easyrsa --batch sign-req client ' + file_name
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to generate certificate ' + str(e)
        return 'Success, certificate for ' + file_name + ' created.'

    def build_ca(self):
        cmd = 'easyrsa --batch build-ca nopass'
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to build ca certificate ' + str(e)
        return 'Success, ca certificate created'
