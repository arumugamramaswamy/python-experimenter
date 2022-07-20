import logging
import logging.config


def configure_logging(level):
    config = {
        # version is required in all configs
        "version": 1,
        "formatters": {
            "standard": {
                "format": "[%(name)s|%(levelname)s|%(asctime)s]%(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
            }
        },
        "loggers": {
            "experimenter": {
                "handlers": ["console"],
                "level": level,
            }
        },
    }

    logging.config.dictConfig(config)
