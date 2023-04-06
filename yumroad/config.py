class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True

class TestConfig(BaseConfig):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class ProdConfig(BaseConfig):
    DEBUG = False

configurations = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}
