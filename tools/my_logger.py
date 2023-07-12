# 开发者：Annona
# 开发时间：2023/7/12 13:53
import logging
import datetime
import time


class MyLogger:
    def __init__(self, log_directory):
        self.log_directory = log_directory
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s_%(funcName)s:%(message)s')

        current_date = datetime.datetime.now().strftime('%Y_%m_%d')
        log_file_path = f'{self.log_directory}/log_{current_date}.txt'
        file_handler = logging.FileHandler(log_file_path,encoding='utf-8',mode ='a+')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)