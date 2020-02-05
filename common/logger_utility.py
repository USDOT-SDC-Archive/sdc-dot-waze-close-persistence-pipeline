import logging
import os

from common.constants import Constants


class LoggerUtility:
    @staticmethod
    def set_level():
        log_format = '%(asctime)-15s %(levelname)s:%(message)s'
        logging.basicConfig(format=log_format)
        logger = logging.getLogger(Constants.LOGGER_NAME)

        try:
            log_level = os.environ[Constants.LOGGER_LOG_LEVEL_ENV_VAR]
        except KeyError:
            log_level = Constants.LOGGER_DEFAULT_LOG_LEVEL

        logger.setLevel(logging.getLevelName(log_level))
        return True

    @staticmethod
    def log(log_level_name, message):
        logger = logging.getLogger(Constants.LOGGER_NAME)
        log_level = getattr(logging, log_level_name.upper())
        logger.log(log_level, message)
