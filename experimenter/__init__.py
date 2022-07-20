from .logger import configure_logging

import os

configure_logging(os.environ.get("LOGLEVEL", "WARNING").upper())

__version__ = "0.1.0"
