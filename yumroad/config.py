import os

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY')

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY', '00000abcdef')

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY', '12345abcdef')
    WTF_CSRF_ENABLED = False

class ProdConfig(BaseConfig):
    DEBUG = False

configurations = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}
