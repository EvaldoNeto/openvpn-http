

class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = '/usr/src/certs'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEV_MODE = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
