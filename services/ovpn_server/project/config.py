
import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = '/usr/src/certs'
    CERT_SERVER_URL = os.environ.get('CERT_SERVER_URL')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEV_MODE = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
