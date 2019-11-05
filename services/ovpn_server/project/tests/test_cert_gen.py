# services/ovpn_server/project/tests/test_cert_gen.py

import os

from project.api.cert_gen import EasyRSA
from project.tests.base import BaseTestCase
from shutil import copy2


class TestCertGen(BaseTestCase):

    def test_build_ca(self):
        """Tests the ca build"""
        pki_path = os.environ.get('EASYRSA_PKI')
        resp = EasyRSA().build_ca()
        os.remove(pki_path + '/ca.crt')
        os.remove(pki_path + '/private/ca.key')
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
        os.remove(req_path + '/ca.crt')
        os.remove(req_path + '/private/ca.key')
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

    def test_sign_req(self):
        """Tests if the .crt file is generated"""
        pki_path = os.environ.get('EASYRSA_PKI')
        EasyRSA().build_ca()
        EasyRSA().req_gen('clien666')
        resp = EasyRSA().sign_req('clien666')
        self.assertIn('Success', resp)
        self.assertTrue(os.path.isfile(pki_path + '/issued/clien666.crt'))
        self.assertTrue(os.path.isfile(pki_path + '/ca.crt'))
        os.remove(pki_path + '/issued/clien666.crt')
        os.remove(pki_path + '/ca.crt')
        os.remove(pki_path + '/private/ca.key')
        os.remove(pki_path + '/private/clien666.key')
        os.remove(pki_path + '/reqs/clien666.req')
        self.assertFalse(os.path.isfile(pki_path + '/issued/clien666.crt'))
        self.assertFalse(os.path.isfile(pki_path + '/ca.crt'))


    def test_ovpn_gen(self):
        """Tests if the .ovpn file is generated"""
        EasyRSA().build_ca()
        EasyRSA().req_gen('clien666')
        EasyRSA().sign_req('clien666')
        pki_path = os.environ.get('EASYRSA_PKI')
        crt_path = pki_path + '/issued/clien666.crt'
        key_path = pki_path + '/private/clien666.key'
        ca_path = pki_path + '/ca.crt'
        resp = EasyRSA().ovpn_gen(crt_path, key_path, ca_path)
        os.remove(pki_path + '/issued/clien666.crt')
        os.remove(pki_path + '/ca.crt')
        os.remove(pki_path + '/private/ca.key')
        os.remove(pki_path + '/private/clien666.key')
        os.remove(pki_path + '/reqs/clien666.req')
        self.assertTrue(os.path.isfile('/usr/src/app/clien666.ovpn'))
        os.remove('/usr/src/app/clien666.ovpn')
        self.assertFalse(os.path.isfile('/usr/src/app/clien666.ovpn'))
