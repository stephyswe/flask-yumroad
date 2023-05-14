import os

folder_path = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv("YUMROAD_SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT", 587)
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", True)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_k1")
    STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_k1")
    STRIPE_WEBHOOK_KEY = os.getenv("STRIPE_WEBHOOK_KEY", "whsec_test_secret")

    SENTRY_DSN = os.getenv("SENTRY_DSN")

    REDIS_URL = os.getenv("REDIS_URL", "redis://:@localhost:6379/0")
    RQ_REDIS_URL = REDIS_URL
    RQ_DASHBOARD_REDIS_URL = RQ_REDIS_URL


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
        os.path.join(folder_path, "dev.db")
    )
    SECRET_KEY = os.getenv("YUMROAD_SECRET_KEY", "00000abcdef")
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    DEBUG = True
    # Don't do anything fancy with the assets pipeline (faster + easier to
    # debug)
    ASSETS_DEBUG = True
    RQ_REDIS_URL = REDIS_URL = os.getenv(
        "REDIS_URL", "redis://:@localhost:6379/0"
    )
    CACHE_TYPE = "simple"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_ENABLED = True


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
        os.path.join(folder_path, "test.db")
    )
    SECRET_KEY = os.getenv("YUMROAD_SECRET_KEY", "12345abcdef")
    WTF_CSRF_ENABLED = False
    STRIPE_WEBHOOK_KEY = "whsec_test_secret"
    ASSETS_DEBUG = True
    # Run jobs instantly, without needing to spin up a worker
    RQ_ASYNC = False
    RQ_CONNECTION_CLASS = "fakeredis.FakeStrictRedis"
    DEBUG_TB_ENABLED = False
    CACHE_TYPE = "null"
    CACHE_NO_NULL_WARNING = True


class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SESSION_PROTECTION = "strong"
    # You should be using HTTPS in production anyway, but if you are not, turn
    # these two off
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    ASSETS_DEBUG = False
    RQ_REDIS_URL = REDIS_URL = os.getenv("REDIS_URL")
    RQ_ASYNC = REDIS_URL is not None
    CACHE_TYPE = "redis"
    CACHE_KEY_PREFIX = "yumroad-"


configurations = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig,
}
