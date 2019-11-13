# services/ovpn_server/project/tests/test_cert_gen.py

import os

from flask import current_app

from project.api.cert_gen import EasyRSA
from project.tests.base import BaseTestCase


class TestCertGen(BaseTestCase):

    def test_build_ca(self):
        """Tests the ca build"""
        pki_path = current_app.config['PKI_PATH']
        resp = EasyRSA().build_ca()
        self.assertIn('Success', resp)
        self.assertTrue(os.path.isfile(f'{pki_path}/ca.crt'))
        self.assertTrue(os.path.isfile(f'{pki_path}/private/ca.key'))
        os.remove(pki_path + '/ca.crt')
        os.remove(pki_path + '/private/ca.key')
        self.assertFalse(os.path.isfile(f'{pki_path}/ca.crt'))
        self.assertFalse(os.path.isfile(f'{pki_path}/private/ca.key'))

    def test_req_gen(self):
        """Tests if the requisition is generated"""
        filename = 'test_client'
        resp = EasyRSA().req_gen(filename)
        pki_path = current_app.config['PKI_PATH']
        self.assertTrue(os.path.isfile(f'{pki_path}/reqs/{filename}.req'))
        self.assertTrue(os.path.isfile(f'{pki_path}/private/{filename}.key'))
        os.remove(f'{pki_path}/reqs/{filename}.req')
        os.remove(f'{pki_path}/private/{filename}.key')
        self.assertFalse(os.path.isfile(f'{pki_path}/reqs/{filename}.req'))
        self.assertFalse(os.path.isfile(f'{pki_path}/private/{filename}.key'))
        self.assertIn('Success', resp)

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
        pki_path = current_app.config['PKI_PATH']
        filename = 'test_client'
        EasyRSA().build_ca()
        EasyRSA().req_gen(filename)
        resp = EasyRSA().sign_req(filename)
        self.assertIn('Success', resp)
        self.assertTrue(os.path.isfile(f'{pki_path}/issued/{filename}.crt'))
        self.assertTrue(os.path.isfile(f'{pki_path}/ca.crt'))
        self.assertTrue(os.path.isfile(f'{pki_path}/reqs/{filename}.req'))
        self.assertTrue(os.path.isfile(f'{pki_path}/private/{filename}.key'))
        self.assertTrue(os.path.isfile(f'{pki_path}/private/ca.key'))
        resp = EasyRSA().revoke(filename)
        os.remove(f'{pki_path}/issued/{filename}.crt')
        os.remove(f'{pki_path}/ca.crt')
        os.remove(f'{pki_path}/private/ca.key')
        os.remove(f'{pki_path}/private/{filename}.key')
        os.remove(f'{pki_path}/reqs/{filename}.req')
        self.assertIn('Success', resp)
        self.assertFalse(os.path.isfile(f'{pki_path}/issued/{filename}.crt'))
        self.assertFalse(os.path.isfile(f'{pki_path}/ca.crt'))
        self.assertFalse(os.path.isfile(f'{pki_path}/reqs/{filename}.req'))
        self.assertFalse(os.path.isfile(f'{pki_path}/private/{filename}.key'))
        self.assertFalse(os.path.isfile(f'{pki_path}/private/ca.key'))

    def test_ovpn_gen(self):
        """Tests if the .ovpn file is generated"""
        filename = 'test_client'
        EasyRSA().build_ca()
        EasyRSA().req_gen(filename)
        EasyRSA().sign_req(filename)
        pki_path = current_app.config['PKI_PATH']
        crt_path = f'{pki_path}/issued/{filename}.crt'
        key_path = f'{pki_path}/private/{filename}.key'
        ca_path = f'{pki_path}/ca.crt'
        ovpn_path = current_app.config['OVPN_CERTS_PATH']
        EasyRSA().ovpn_gen(crt_path, key_path, ca_path)
        os.remove(f'{pki_path}/issued/{filename}.crt')
        os.remove(f'{pki_path}/ca.crt')
        os.remove(f'{pki_path}/private/ca.key')
        os.remove(f'{pki_path}/private/{filename}.key')
        os.remove(f'{pki_path}/reqs/{filename}.req')
        self.assertTrue(os.path.isfile(f'{ovpn_path}/{filename}.ovpn'))
        os.remove(f'{ovpn_path}/{filename}.ovpn')
        EasyRSA().revoke(filename)
        self.assertFalse(os.path.isfile(f'{ovpn_path}/{filename}.ovpn'))
        self.assertFalse(os.path.isfile(f'{pki_path}/issued/{filename}.crt'))
        self.assertFalse(os.path.isfile(f'{pki_path}/ca.crt'))
        self.assertFalse(os.path.isfile(f'{pki_path}/reqs/{filename}.req'))
        self.assertFalse(os.path.isfile(f'{pki_path}/private/{filename}.key'))
        self.assertFalse(os.path.isfile(f'{pki_path}/private/ca.key'))

    def test_sign_cert_server(self):
        pki_path = current_app.config['PKI_PATH']
        filename = 'test_server'
        EasyRSA().build_ca()
        EasyRSA().req_gen(filename)
        resp = EasyRSA().sign_req(filename, is_server=True)
        self.assertIn('Success', resp)
        self.assertTrue(os.path.isfile(f'{pki_path}/issued/{filename}.crt'))
        self.assertTrue(os.path.isfile(f'{pki_path}/ca.crt'))
        self.assertTrue(os.path.isfile(f'{pki_path}/reqs/{filename}.req'))
        self.assertTrue(os.path.isfile(f'{pki_path}/private/{filename}.key'))
        self.assertTrue(os.path.isfile(f'{pki_path}/private/ca.key'))
        resp = EasyRSA().revoke(filename)
        os.remove(f'{pki_path}/issued/{filename}.crt')
        os.remove(f'{pki_path}/ca.crt')
        os.remove(f'{pki_path}/private/ca.key')
        os.remove(f'{pki_path}/private/{filename}.key')
        os.remove(f'{pki_path}/reqs/{filename}.req')
        self.assertIn('Success', resp)
        self.assertFalse(os.path.isfile(f'{pki_path}/issued/{filename}.crt'))
        self.assertFalse(os.path.isfile(f'{pki_path}/ca.crt'))
        self.assertFalse(os.path.isfile(f'{pki_path}/reqs/{filename}.req'))
        self.assertFalse(os.path.isfile(f'{pki_path}/private/{filename}.key'))
        self.assertFalse(os.path.isfile(f'{pki_path}/private/ca.key'))
