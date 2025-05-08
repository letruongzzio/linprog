"""
This module sets up a logger for the application. It configures the logging format,
log level, and log file location. The logger can be used throughout the application
to log messages for debugging and tracking purposes.
"""

import os
import sys
import logging

LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format=LOGGING_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
