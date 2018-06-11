import os
import tempfile


class Config(object):
    """Parent configuration class."""

    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', default='Secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    @property
    def qualified_name(self):
        module_name = self.__module__
        class_name = self.__class__.__name__
        return "{}.{}".format(module_name, class_name)


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
    'development': DevelopmentConfig().qualified_name,
    'test': TestingConfig().qualified_name,
    'production': ProductionConfig().qualified_name
}
