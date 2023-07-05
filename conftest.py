# 开发者：Annona
# 开发时间：2023/6/5 14:42
import random
import time

import allure
import pytest

from data_driver.deal_xml import set_xml, set_xml_string
from tools.tools import Tools


@allure.title('交易初始化')
@pytest.fixture(scope='session', autouse=True)
def init():
    """
        先查询一下数据库中的ttrd_fix_setflag.init_date是否已经初始化到当前系统日期;
        (1)如果没有初始化，则发送初始化，然后再做交易；
        (2)如果已经初始化了，则不需要做任何操作，直接做交易；
    :return:
    """
    global step_init, tools
    tools = Tools()
    # 可以指定只在自动化项目开始运行之前执行一下初始化
    long_date, local_date, local_time = tools.get_system_time()
    sql = 'select t.init_date from ttrd_fix_setflag t'
    result_list = tools.oracle_link(sql)
    if result_list['INIT_DATE'] == local_date:
        pass
    else:
        step_init = 'data/shg_fix/DS_1100_STEP_INIT.xml'
        set_xml(step_init,
                {'sendDateTime': long_date, 'initDate': local_date})
        data = set_xml_string(step_init)
        result = tools.send_post(1100, data)
        print('初始化响应信息：',result)
