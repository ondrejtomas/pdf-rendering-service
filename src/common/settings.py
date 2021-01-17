# Standard Library

# Third Party
from starlette.config import Config

config = Config(".env")

# service
SERVICE_HOST = config("SERVICE_HOST", cast=str, default="127.0.0.1")
SERVICE_LOG_CONF = config("SERVICE_LOG_CONF", cast=str, default="config/logging.json")
SERVICE_LOG_LEVEL = config("SERVICE_LOG_LEVEL", cast=str, default="INFO")
SERVICE_PORT = config("SERVICE_PORT", cast=int, default=8000)

# database
DATABASE_HOST = config("DATABASE_HOST", cast=str, default="postgres")
DATABASE_NAME = config("DATABASE_NAME", cast=str, default="pdf_rendering_service")
DATABASE_PASSWORD = config("DATABASE_PASSWORD", cast=str, default="password")
DATABASE_PORT = config("DATABASE_PORT", cast=int, default=5432)
DATABASE_USERNAME = config("DATABASE_USERNAME", cast=str, default="stolon")

# message queue
MESSAGE_QUEUE_HOST = config("MESSAGE_QUEUE_HOST", cast=str, default="rabbitmq")
MESSAGE_QUEUE_PASSWORD = config("MESSAGE_QUEUE_PASSWORD", cast=str, default="guest")
MESSAGE_QUEUE_PORT = config("MESSAGE_QUEUE_PORT", cast=int, default=5672)
MESSAGE_QUEUE_USERNAME = config("MESSAGE_QUEUE_USERNAME", cast=str, default="guest")

# rendering
RENDERING_PNG_MAX_HEIGHT = config("RENDERING_PNG_MAX_HEIGHT", cast=int, default=1200)
RENDERING_PNG_MAX_WIDTH = config("RENDERING_PNG_MAX_WIDTH", cast=int, default=1600)

# TODO: enable secured connection
# SSL_CA_CERTS = config("SSL_CA_CERTS", cast=str, default=None)
# SSL_CERTFILE = config("SSL_CERTFILE", cast=str, default=None)
# SSL_CERT_REQS = config("SSL_CERT_REQS", cast=int, default=CERT_OPTIONAL)
# SSL_CIPHERS = config("SSL_CIPHERS", cast=str, default=None)
# SSL_KEYFILE = config("SSL_KEYFILE", cast=str, default=None)
# SSL_VERSION = config("SSL_VERSION", cast=int, default=None)
