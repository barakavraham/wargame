import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Auth:
    CLIENT_ID = ('107154101011-vfaqeq3fi2ult8seasotblrq86cdds4h' '.apps.googleusercontent.com')
    CLIENT_SECRET = '7Dqz5g9dGPeoFafrTV9hq26D'
    REDIRECT_URI = 'https://localhost:5000/auth/google'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['https://www.googleapis.com/auth/userinfo.email']


class Config:
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")


class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")


config = {
"dev": DevConfig,
"prod": ProdConfig,
"default": DevConfig
}