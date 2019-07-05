
import os


class BaseConfig:
    """Base configuration"""
    TESTING = False
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    MONGO_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    MONGO_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    MONGO_DATABASE_URI = os.environ.get('DATABASE_URL')
