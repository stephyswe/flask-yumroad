import os

folder_path = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT', 587)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(folder_path, 'dev.db'))
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY', '00000abcdef')

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(folder_path, 'test.db'))
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY', '12345abcdef')
    WTF_CSRF_ENABLED = False

class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SESSION_PROTECTION = "strong"
    # You should be using HTTPS in production anyway, but if you are not, turn
    # these two off
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

configurations = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}
