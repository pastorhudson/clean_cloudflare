import configparser
import os
import logging
import colorlog
from datetime import datetime


def setup_logger(logger_name):
    # Create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Create a color formatter for the console
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    # Create a console handler and set the color formatter
    ch = logging.StreamHandler()
    ch.setFormatter(color_formatter)

    # Create a file handler and set level to debug
    date = datetime.now().strftime('%Y-%m-%d')
    fh = logging.FileHandler(f'{date}-log.txt')

    # Create a standard formatter for the file
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(file_formatter)

    # Add handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


logger = setup_logger(__name__)


def check_config():
    # Check if the file does not exist
    if not os.path.isfile('config.ini'):

        # Create a configparser object
        config = configparser.ConfigParser()

        # Populate the configparser object with your data
        config['app'] = {
            ';Your Cloudflare account email': '',
            'email': 'you@email.com',
            ';Your Cloudflare API Key': '',
            'api_key': '123',
            ';Your Cloudflare Account ID Found on Right side of Stream Page': '',
            'account_id': '123',
            ';A list of whitelisted video ids that will be skipped and not deleted': '',
            'whitelist': ['123', '456'],

        }

        # Write the populated configparser object to config.ini file
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        raise Exception("Configuration not found.\n"
                        "One has been created for you. Please edit the config.ini with your own settings.")
    logger.info("Config File Found")
    return "Config found - Success"


def get_config():
    """
    Reads and returns the configuration from the 'config.ini' file.

    :return: The configuration as a configparser.ConfigParser object.
    """
    check_config()

    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


if __name__ == '__main__':
    print(check_config())