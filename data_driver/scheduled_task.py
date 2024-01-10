# 开发者：Annona
# 开发时间：2024/1/10 14:35
import datetime
import os

import configparser
import schedule
import time
import subprocess

# # 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')


def run_task():
    command = config['Task']['command']
    try:
        result = subprocess.run(command, shell=True)

        if result.returncode == 0:
            print("任务执行成功")
        else:
            print("任务执行失败")

    except Exception as e:
        print("任务执行错误:", str(e))


# 获取间隔时间
interval = 60
print("任务将会每隔{}秒执行一次".format(interval))

# 设置定时任务
# schedule.every(timedelta(seconds=interval)).do(run_task)
schedule.every(interval).seconds.do(run_task)
while True:
    schedule.run_pending()
    time.sleep(1)