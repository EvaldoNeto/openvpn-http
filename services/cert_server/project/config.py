import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = '/usr/src/certs'
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEV_MODE = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
