# 开发者：Annona
# 开发时间：2024/1/10 15:52
# 该任务用于查询上交所固定收益平台确定报价的行情

# 读取配置文件
import configparser

# 读取配置文件
import subprocess
import time

import schedule


config = configparser.ConfigParser()
config.read('config.ini')


def run_shg_task():
    # 获取执行命令
    command = config['Task']['command']
    print(command)
    try:
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            print("任务执行成功")
        else:
            print("任务执行失败")
    except Exception as e:
        print(e)

run_shg_task()