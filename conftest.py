# 开发者：Annona
# 开发时间：2023/6/5 14:42
import random
import time

import allure
import pytest

from data_driver.deal_xml import set_xml, set_xml_string
from tools.tools import Tools


@allure.step('交易初始化')
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


# @allure.step('上交所协商成交申报')
# @pytest.fixture(scope='function')
# def shg_xscj_sb():
#     global shg_xscj_path
#     shg_xscj_path = 'data/shg_fix/DS_1101_SHG_Fix_XSCJ.xml'
#     # 获取当前系统的时间
#     long_date, local_date, local_time = tools.get_system_time()
#     # 委托表中的主键，使用时间戳表示
#     sysordid = str(int(time.time()))
#
#     # 使用random,生成需要每次不能重复的约定号
#     match_no = str(random.randint(100, 999))
#
#     set_xml(shg_xscj_path,
#             {'sendDateTime': long_date, 'ordDate': local_date, 'ordTime': local_time, 'matchNo': match_no,
#              'sysOrdID': sysordid})
#     data = set_xml_string(shg_xscj_path)
#     result = tools.send_post(1101, data)
#     time.sleep(2)
#     with allure.step('数据库断言'):
#         sql = f'select t.ordstatus from ttrd_fix_order t  where t.SYSORDID={sysordid}'
#         result_list = tools.oracle_link(sql)
#         with allure.step('预期结果：ord_status=5'):
#             ord_status = result_list[0][0]
#         with allure.step(f'实际结果：ord_status={ord_status}'):
#             assert ord_status == 5
#     return tools, sysordid, match_no
