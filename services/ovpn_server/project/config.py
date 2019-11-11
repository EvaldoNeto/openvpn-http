
import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = '/usr/src/certs'
    PKI_PATH = os.environ.get('EASYRSA_PKI')
    CERT_SERVER_URL = os.environ.get('CERT_SERVER_URL')
    OVPN_CERTS_PATH = os.environ.get('OVPN_FILES')
    CRT_CERTS_PATH = os.environ.get('CRT_FILES')
    OPENVPN = os.environ.get('OPENVPN')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEV_MODE = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
