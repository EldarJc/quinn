import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Set base directory of the app
BASEDIR = Path(__file__).parent.parent

# Logging configuration
LOGGING_LVL = os.getenv("LOGGING_LEVEL", "INFO")
LOGGING_FILE = BASEDIR / "logs/app.log"
LOGGING_FILE.parent.mkdir(parents=True, exist_ok=True)


class BaseConfig:
    """Base Configuration"""

    # Flask Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    # ImageKit API credentials
    IMAGEKIT_PRIVATE_KEY = os.environ.get("IMAGEKIT_PRIVATE_KEY")
    IMAGEKIT_URL_ENDPOINT = os.environ.get("IMAGEKIT_URL_ENDPOINT")

    # Flask-JWT-Extended
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_VERIFY_SUB = False

    # Config API documents
    API_TITLE = "quinn API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {
                "Bearer Auth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "bearerFormat": "JWT",
                    "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
                }
            }
        },
    }

    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging configuration
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s",
            },
            "detailed": {
                "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "detailed",
                "level": LOGGING_LVL,
                "filename": LOGGING_FILE,
                "maxBytes": 1024 * 1024 * 10,  # 10MB
                "backupCount": 5,
            },
        },
        "root": {
            "handlers": ["stdout", "file"],
            "level": LOGGING_LVL,
        },
    }


class DevConfig(BaseConfig):
    """Development Configuration"""

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_DEV")


class TestConfig(BaseConfig):
    """Test Configuration"""

    TESTING = True

    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST")


config_options = {
    "development": DevConfig,
    "testing": TestConfig,
}
