# services/ovpn_server/project/tests/test_cert_gen.py

import os

from project.api.cert_gen import EasyRSA
from project.tests.base import BaseTestCase
from shutil import copy2


class TestCertGen(BaseTestCase):

    def test_build_ca(self):
        """Tests the ca build"""
        resp = EasyRSA().build_ca()
        self.assertIn('Success', resp)

    def test_req_gen(self):
        """Tests if the requisition is generated"""
        resp = EasyRSA().req_gen('test_client')
        req_path = os.environ.get('EASYRSA_PKI')
        self.assertTrue(os.path.isfile(req_path + '/reqs/test_client.req'))
        self.assertTrue(os.path.isfile(req_path + '/private/test_client.key'))
        os.remove(req_path + '/reqs/test_client.req')
        os.remove(req_path + '/private/test_client.key')
        self.assertFalse(os.path.isfile(req_path + '/private/test_client.key'))
        self.assertFalse(os.path.isfile(req_path + '/reqs/test_client.req'))
        self.assertIn('Success', resp)

    def test_cert_gen(self):
        """Tests if the certificate is generated"""
        EasyRSA().build_ca()
        EasyRSA().req_gen('test_client')
        req_path = os.environ.get('EASYRSA_PKI')
        copy2(req_path + '/reqs/test_client.req', os.environ.get('REQ_PATH'))
        resp = EasyRSA().cert_gen('test_client')
        self.assertIn('Success', resp)
        self.assertTrue(os.path.isfile(req_path + '/issued/test_client.crt'))
        os.remove(req_path + '/reqs/test_client.req')
        os.remove(os.environ.get('REQ_PATH') + '/test_client.req')
        os.remove(req_path + '/issued/test_client.crt')
        self.assertFalse(os.path.isfile(os.environ.get('REQ_PATH') +
                                        '/test_client.req'))
        self.assertFalse(os.path.isfile(req_path + '/reqs/test_client.req'))
        self.assertFalse(os.path.isfile(req_path + '/issued/test_client.crt'))

    """
    def test_gen_dh(self):
        \"""Tests if the Diffie-Hellman certificate is generated""\"
        resp = EasyRSA().gen_dh()
        req_path = os.environ.get('EASYRSA_PKI')
        self.assertIn('Success', resp)
        self.assertTrue(os.path.isfile(req_path + '/dh.pem'))
    """
