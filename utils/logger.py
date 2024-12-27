import logging
from flask import Flask

# Create a logger instance
logger = logging.getLogger("my_logger")

def configure_global_logger():
    # Set log level
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()

    # Define a custom log format
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

# Configure the logger before the app starts
configure_global_logger()