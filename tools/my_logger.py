# 开发者：Annona
# 开发时间：2023/7/12 13:53
import logging
import datetime


def my_logger(log_directory):
    # 日志器，创建日志器
    logger = logging.getLogger()
    # 设置日志级别
    logger.setLevel(logging.INFO)
    # 判断如果没有定义过日志处理器，则进入到下面的逻辑
    if not logger.handlers:
        current_date = datetime.datetime.now().strftime('%Y_%m_%d')
        log_file_path = f'{log_directory}/log_{current_date}.txt'
        # 创建文本处理器
        fh = logging.FileHandler(log_file_path, encoding='utf-8', mode='a+')
        logger.addHandler(fh)

        fhfmt = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s_%(funcName)s:%(message)s'
        fhfmtFH = logging.Formatter(fhfmt)
        fh.setFormatter(fhfmtFH)
    return logger
