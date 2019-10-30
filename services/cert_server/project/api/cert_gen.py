# services/cert_server/project/apit/cert_gen.py

import subprocess
import os


class EasyRSA:
    req_path = os.environ.get('REQ_PATH')

    def __init__(self):
        pass

    def cert_gen(self, file_name):
        cmd = 'easyrsa --batch import-req ' + self.req_path + '/' + \
              file_name + '.req ' + file_name
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to import requisition ' + str(e)
        cmd = 'easyrsa --batch sign-req client ' + file_name
        try:
            subprocess.check_output(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            return 'Fail to generate certificate ' + str(e)
        return 'Success, certificate for ' + file_name + ' created.'
