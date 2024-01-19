import os
import sys


serverdir = os.path.abspath(os.path.dirname(__file__))

check_dir = serverdir
while not os.path.exists(os.path.join(check_dir, 'server')):
    check_dir = os.path.dirname(check_dir)
root_project_dir = check_dir

# Look for config.env on the same level as config.py
config_env_path = os.path.join(serverdir, 'config.env')
if os.path.exists(config_env_path):
    print('Importing environment from .env file')
    for line in open(config_env_path):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")
else:
    print('config.env file not found, please read README.md for config.env file structure')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
        'sqlite:///' + os.path.join(root_project_dir, 'data-dev.sqlite'))

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL',
        'sqlite:///' + os.path.join(root_project_dir, 'data-test.sqlite'))

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN TESTING MODE.  \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
        'sqlite:///' + os.path.join(root_project_dir, 'data.sqlite'))

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET KEY IS NOT SET!'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
