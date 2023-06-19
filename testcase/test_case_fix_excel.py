# 开发者：Annona
# 开发时间：2023/6/19 14:50
import random
import time

import allure
import pytest

from data_driver.deal_excel import read_excel
from data_driver.deal_xml import set_xml, set_xml_string
from tools.tools import Tools


def setup_module(module):
    global tools
    tools = Tools()


@pytest.mark.parametrize('data', read_excel('data/step_case.xlsx'))
def test_shg_fix_xscj(data):
    if data[1] is not None:
        allure.dynamic.feature(data[1])
    if data[2] is not None:
        allure.dynamic.story(data[2])
    if data[3] is not None:
        allure.dynamic.title(data[3])
    if data[4] is not None:
        allure.dynamic.description(data[4])
    if data[5] is not None:
        allure.dynamic.severity(data[5])
    # 获取当前行数
    row_num = data[0] + 1
    # 获取当前系统的时间
    long_date, local_date, local_time = tools.get_system_time()
    print(data)
    # 将从excel中读取的数据放入参数中
    action = data[6]
    change_dic = eval(data[8])
    if action == '1101':
        sysordid = str(int(time.time()))
        # 使用random,生成需要每次不能重复的约定号
        match_no = str(random.randint(100, 999))
        change_dic['matchNo'] = match_no
        change_dic['sendDateTime'] = long_date
        change_dic['ordDate'] = local_date
        change_dic['ordTime'] = local_time
        change_dic['sysOrdID'] = sysordid
    set_xml(data[7],change_dic)
    data = set_xml_string(data[7])
    result = tools.send_post(action, data)
    time.sleep(1)
    print(data)
    print(result)
# if __name__ == '__main__':
#     pytest.main(['-s'])
