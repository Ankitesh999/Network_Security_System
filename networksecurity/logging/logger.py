import logging
import os
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)


# Create and configure a reusable logger instance
logger = logging.getLogger("networksecurity")
logger.setLevel(logging.INFO)


# Add file handler if not already present
if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setFormatter(logging.Formatter('[%(asctime)s] - %(lineno)d %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

# Add stream handler if not already present
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('[%(asctime)s] - %(lineno)d %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(stream_handler)

