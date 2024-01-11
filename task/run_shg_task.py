# 开发者：Annona
# 开发时间：2024/1/10 15:52
# 该任务用于查询上交所固定收益平台确定报价的行情
# 读取配置文件
import configparser
import subprocess

from constant.constant import MY_LOGGER

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')


def run_shg_command():
    # 获取执行命令
    command = config['Task']['command']
    try:
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            MY_LOGGER.error("任务执行成功!")
        else:
            MY_LOGGER.error("任务执行成功!")
    except Exception as e:
        MY_LOGGER.error(e)
