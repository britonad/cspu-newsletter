import os

BASE_DIR = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')


class Common:
    DEBUG = True
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_DOMAIN_NAME = os.environ.get('MAILGUN_DOMAIN_NAME')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class Dev(Common):
    BASIC_AUTH_USERNAME = 'test'
    BASIC_AUTH_PASSWORD = 'test'
    MAILING_LIST = os.environ.get('MAILING_LIST')


class Prod(Common):
    DEBUG = False
    MAILING_LIST = os.environ.get('MAILING_LIST')
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')
