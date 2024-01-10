# 开发者：Annona
# 开发时间：2023/6/5 14:42
import os
import threading
import time

import pytest
import schedule

from task.run_shg_task import run_shg_task


def run_test_task():
    print('开始自动化测试任务')
    pytest.main(['-v', '-s', '--alluredir', './result', '--clean-alluredir'])
    # 将.json文件的测试报告转为html格式
    # system函数可以将字符串转化成命令在服务器上运行
    os.system('allure generate ./result -o ./report --clean')
def run_shg_task1():
    # 设置定时任务
    print('开始定时轮询任务')
    # schedule.every(timedelta(seconds=interval)).do(run_task)
    schedule.every(5).seconds.do(run_shg_task)
    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == '__main__':
    # 创建线程
    test_thread = threading.Thread(target=run_test_task)
    polling_thread = threading.Thread(target=run_shg_task1)

    # 启动线程
    test_thread.start()
    polling_thread.start()

    # 等待线程结束
    test_thread.join()
    polling_thread.join()

    # print("所有任务完成")
    # 生成json类型的测试报告
    # pytest.main(['-v', '-s', '--alluredir', './result', '--clean-alluredir'])
    # # 将.json文件的测试报告转为html格式
    # # system函数可以将字符串转化成命令在服务器上运行
    # os.system('allure generate ./result -o ./report --clean')
