import logging
from datetime import datetime


class LogHelper:
    def log_error(self, message):
        logging.error(f'[{self._get_date()}] {message}')

    def log_info(self, message):
        logging.info(f'[{self._get_date()}] {message}\n')

    def _get_date(self):
        # format: y-m-d h:m:s:ms
        return str(datetime.now())[:23]
