# Standard Imports
import sys
import os

# Third Party Imports
from loguru import logger

# Local Imports
from server.config import root_project_dir, Config


def setup_logger():
    # Obtain logger details from config
    environment = os.getenv("FLASK_CONFIG", "production")
    diagnose = False if environment == "production" else True
    logging_level = os.getenv("LOGGING_LEVEL", "stuff")

   # Configure Loguru logger
    logger_format = "<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level}</level> | {message}"
    logger.add(sys.stderr, colorize=True, diagnose=diagnose, format=logger_format, level=logging_level)
    
    # Check if directory exists
    if not os.path.exists(f"{root_project_dir}/data/logs"):
        os.makedirs(f"{root_project_dir}/data/logs")
    
    # Add a log file
    logger.add(
        f"{root_project_dir}/data/logs/server.log",
        diagnose=diagnose, retention="10 days",
        enqueue=True, 
        #compression="zip",
        format=logger_format,
        level="INFO")
