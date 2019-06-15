import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class DevConfig:
    CONFIG_NAME = 'dev'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = (os.environ.get('SQLALCHEMY_DATABASE_URI')
                               or 'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'


class TestingConfig:
    CONFIG_NAME = 'testing'
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_FILE = os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLALCHEMY_DATABASE_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = ''
    WTF_CSRF_ENABLED = False


config = {
    'development': DevConfig,
    'testing': TestingConfig
}
