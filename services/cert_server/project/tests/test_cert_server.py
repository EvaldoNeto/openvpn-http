# services/ovpn_server/project/tests/test_ovpn_server.py

import os
import json
import io

from flask import current_app

from project.tests.base import BaseTestCase


class TestOvpnServer(BaseTestCase):

    def test_certificates(self):
        with self.client:
            pki_path = current_app.config['PKI_PATH']
            response = self.client.post(
                '/cert/upload',
                data={
                    'file': (io.BytesIO(b'test'), 'test_cert.req'),
                    'cert': 'False'
                },
                content_type='multipart/form-data'
            )
            data = json.loads(response.data.decode())
            self.assertIn('file uploaded', data['message'])
            self.assertEqual(response.status_code, 200)
            self.assertTrue(os.path.isfile(f'{pki_path}/reqs/test_cert.req'))
            os.remove(f'{pki_path}/reqs/test_cert.req')
            self.assertFalse(os.path.isfile(f'{pki_path}/reqs/test_cert.req'))

    def test_certificate_no_file(self):
        """
        Tests response when there is no file being sent
        """
        with self.client:
            response = self.client.post(
                '/cert/upload',
                data={}
            )
            data = json.loads(response.data.decode())
            self.assertIn('No file', data['message'])
            self.assertEqual(response.status_code, 400)

    def test_certificates_invalid_file(self):
        """
        Tests response when an invalid file is sent
        """
        with self.client:
            response = self.client.post(
                '/cert/upload',
                data={'file': (io.BytesIO(str.encode('test')), 'test.txt')}
            )
            data = json.loads(response.data.decode())
            self.assertIn('Not a valid file', data['message'])
            self.assertEqual(response.status_code, 400)
