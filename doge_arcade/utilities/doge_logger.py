import logging
from logging.handlers import RotatingFileHandler

class DogeLogger:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_logger()
        return cls._instance

    @staticmethod
    def _create_logger():
        # Create a logger
        logger = logging.getLogger("DogeLogger")
        logger.setLevel(logging.DEBUG)

        # Create handlers (e.g., rotating file handler)
        handler = RotatingFileHandler("doge-os.log", maxBytes=10000, backupCount=5)
        handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(handler)

        return logger
