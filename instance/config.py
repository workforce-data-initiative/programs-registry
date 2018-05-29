import os
import tempfile


class Config(object):
    """Parent configuration class."""

    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET = os.environ.get('SECRET', 'Secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    """Configurations for Development."""

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    """Configurations for Testing."""

    TESTING = True
    DB_FILE_DESCRIPTOR, DATABASE = tempfile.mkstemp(suffix='.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATABASE)


class ProductionConfig(Config):
    """Configurations for Production."""

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
