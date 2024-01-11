# 开发者：Annona
# 开发时间：2023/6/5 14:42
import os
import threading
import time
import pytest
import schedule

from task.run_shg_task import run_shg_command
# 读取配置文件
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 创建事件对象
stop_polling_event = threading.Event()


def run_test_task():
    print('开始自动化测试任务')
    # 生成json类型的测试报告
    pytest.main(['-v', '-s', '--alluredir', './result', '--clean-alluredir'])
    # 将.json文件的测试报告转为html格式
    # system函数可以将字符串转化成命令在服务器上运行
    os.system('allure generate ./result -o ./report --clean')

    # 设置事件对象,通知轮询线程可以结束了
    stop_polling_event.set()


def run_shg_task():
    print('开始定时轮询任务')
    interval = int(config['Task']['interval_shg'])

    schedule.every(interval).seconds.do(run_shg_command)
    while not stop_polling_event.is_set():
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    # 创建线程
    test_thread = threading.Thread(target=run_test_task)
    polling_thread = threading.Thread(target=run_shg_task)

    # 启动线程
    test_thread.start()
    polling_thread.start()

    # 等待线程结束
    test_thread.join()
    polling_thread.join()

    print("所有任务完成")
