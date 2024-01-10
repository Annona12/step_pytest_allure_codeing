# 开发者：Annona
# 开发时间：2024/1/10 15:52
import os

import pytest


def run_test_task():
    pytest.main(['-v', '-s', '--alluredir', './result', '--clean-alluredir'])
    # 将.json文件的测试报告转为html格式
    # system函数可以将字符串转化成命令在服务器上运行
    os.system('allure generate ./result -o ./report --clean')
