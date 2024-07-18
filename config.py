import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask security configuration options
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "secret"
    )

    # SQLAlchemy configuration options
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SLOW_DB_QUERY_TIME = 0.5

    # Application configuration options
    ORGANIZATION_NAME = (
        os.environ.get("ORGANIZATION_NAME") or "Agri Trans"
    )

    # File upload configuration options
    FARMER_PROFILE_UPLOAD_PATH = os.path.join(
        basedir + "/app/static/images/farmers/"
    )
    LOADER_PROFILE_UPLOAD_PATH = os.path.join(
        basedir + "/app/static/images/loaders/"
    )
    DRIVER_PROFILE_UPLOAD_PATH = os.path.join(
        basedir + "/app/static/images/drivers/"
    )
    RETAILER_PROFILE_UPLOAD_PATH = os.path.join(
        basedir + "/app/static/images/retailers/"
    )
    ADMINISTRATOR_PROFILE_UPLOAD_PATH = os.path.join(
        basedir + "/app/static/images/administrators/"
    )

    UPLOAD_EXTENSIONS = [".jpg", ".gif", ".jpeg", ".png", ".avif", ".webp"]

    # Mail connection configuration options
    MAIL_BACKEND = "smtp"
    MAIL_SERVER = "smtp.zoho.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_TIMEOUT = None

    # Mail Credentials Settings
    MAIL_DEFAULT_SENDER = "Agri Trans <info@jisortublow.co.ke>"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "info@jisortublow.co.ke")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "phOhsj3-")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVELOPMENT_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "development.db")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite://"
    )


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    DB_NAME = os.environ.get("DB_NAME") or "safiri"
    DB_USERNAME = os.environ.get("DB_USERNAME") or "root"
    DB_HOST = os.environ.get("DB_HOST") or "localhost"
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or "MySQLXXX-123a8910"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("PRODUCTION_DATABASE_URL")
        or f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
        + f"/{DB_NAME}"
    )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
