# Standard Library
from json import load
from logging import basicConfig, config, debug, info

# Local
from src.common import settings


def setup_logging(config_path: str = settings.SERVICE_LOG_CONF):
    try:
        with open(config_path, 'rt') as config_file:
            config_dict = load(config_file)
        config.dictConfig(config_dict)
        info(f"Using {config_path} for configuration.")
    except Exception as exp:
        basicConfig(level=settings.LOG_LEVEL)
        info("Cannot find log configuration, using default configuration.")
        debug(exp)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
