import os

from dotenv import load_dotenv

load_dotenv()  # load variables from my .env file


def _normalise_database_url(database_url):
    """Convert legacy postgres URLs to the SQLAlchemy-compatible format."""
    if database_url and database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg2://", 1)
    return database_url


def _development_database_uri(default="sqlite:///site.db"):
    """Return a safe local database URI for development and testing."""
    database_url = _normalise_database_url(os.environ.get("DEV_DATABASE_URL"))
    if database_url and database_url.startswith("postgresql"):
        return database_url
    return default


def _production_database_uri():
    """Return the production database URI from the environment."""
    database_url = _normalise_database_url(os.environ.get("DATABASE_URL"))
    return database_url or "sqlite:///site.db"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = _development_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    SECURITY_PEPPER = os.environ.get("SECURITY_PEPPER", "dev-pepper")

    BIO_ENCRYPTION_KEY = os.environ.get("BIO_ENCRYPTION_KEY")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "lax"

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "unlockedtakeaction@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    GOOGLE_CALENDAR_ID = os.environ.get("GOOGLE_CALENDAR_ID")

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = _development_database_uri()


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = _production_database_uri()

    @classmethod
    def init_app(cls, app):
        assert os.environ.get("SECRET_KEY"), "SECRET_KEY is missing in prod"
        assert os.environ.get("SECURITY_PEPPER"), "SECURITY_PEPPER is missing in prod"
        assert os.environ.get("BIO_ENCRYPTION_KEY"), "BIO_ENCRYPTION_KEY is missing in prod"
        assert os.environ.get("GOOGLE_API_KEY"), "GOOGLE_API_KEY is missing in prod"
        assert os.environ.get("DATABASE_URL"), "DATABASE_URL is missing in prod"


# environment setup
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
