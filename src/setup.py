"""Setup file"""
from datetime import datetime
from loguru import logger as log


class Config:
    """Main Config for logging"""
    logger = None

    def __init__(self, logger=None):
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.logger = logger or log
        self.logger.add(f'logs/{current_time}.log')
        try:
            self.logger.info('Starting Log')
        except Exception as e:
            self.logger.error(e)
