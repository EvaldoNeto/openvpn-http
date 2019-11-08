# services/ovpn_server/project/tests/test_ovpn_server.py

import os
import json
import io

from project.tests.base import BaseTestCase


class TestOvpnServer(BaseTestCase):

    def test_certificates(self):
        with self.client:
            req_path = os.environ.get('REQ_PATH')
            response = self.client.post(
                '/cert/upload',
                data={'file': (io.BytesIO(b'test'), 'test_cert.ovpn')}
            )
            data = json.loads(response.data.decode())
            self.assertIn('file uploaded', data['message'])
            self.assertEqual(response.status_code, 200)
            self.assertTrue(os.path.isfile(req_path + '/test_cert.ovpn'))
            os.remove(req_path + '/test_cert.ovpn')
            self.assertFalse(os.path.isfile(req_path + '/test_cert.ovpn'))

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
