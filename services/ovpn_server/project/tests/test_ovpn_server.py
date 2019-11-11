# services/ovpn_server/project/tests/test_ovpn_server.py

import os
import json
import io

from flask import current_app

from project.tests.base import BaseTestCase


class TestOvpnServer(BaseTestCase):

    def test_certificates(self):
        with self.client:
            filename = 'test_cert.crt'
            crt_path = current_app.config['CRT_CERTS_PATH']
            response = self.client.post(
                '/ovpn/certs',
                data={'file': (io.BytesIO(b'test'), filename)}
            )
            data = json.loads(response.data.decode())
            self.assertIn(f'{filename} saved', data['message'])
            self.assertEqual(response.status_code, 200)
            self.assertTrue(os.path.isfile(f'{crt_path}/{filename}'))
            os.remove(f'{crt_path}/{filename}')
            self.assertFalse(os.path.isfile(f'{crt_path}/{filename}'))

    def test_certificate_no_file(self):
        """
        Tests response when there is no file being sent
        """
        with self.client:
            response = self.client.post(
                '/ovpn/certs',
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
                '/ovpn/certs',
                data={'file': (io.BytesIO(str.encode('test')), 'test.txt')}
            )
            data = json.loads(response.data.decode())
            self.assertIn('Not a valid file', data['message'])
            self.assertEqual(response.status_code, 400)
