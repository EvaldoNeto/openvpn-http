import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = '/usr/src/certs'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PKI_PATH = os.environ.get('EASYRSA_PKI')
    REQ_PATH = os.environ.get('REQ_PATH')
    OVPN_SERVER_URL = os.environ.get('OVPN_SERVER_URL')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEV_MODE = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
