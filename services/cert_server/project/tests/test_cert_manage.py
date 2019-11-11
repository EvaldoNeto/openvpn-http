# services/cert_server/project/tests/test_cert_manage.py

import os

from flask import current_app
from werkzeug.datastructures import FileStorage

from project.tests.base import BaseTestCase
from project.api.cert_manage import save_file


class TestCertManage(BaseTestCase):

    def not_testing_test_save_file(self):
        filename = 'test.req'
        with open(filename, 'rw') as fp:
            pki_path = current_app.config['PKI_PATH']
            file = FileStorage(fp)
            resp, stat = save_file(file)
            self.assertIn('saved', resp['message'])
            self.assertEqual(stat, 200)
            self.assertEqual('success', resp['status'])
            self.assertTrue(os.path.isfile(f'{pki_path}/reqs/{filename}'))
            os.remove(f'{pki_path}/reqs/{filename}')
            self.assertFalse(os.path.isfile(f'{pki_path}/reqs/{filename}'))
