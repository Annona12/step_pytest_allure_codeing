# 开发者：Annona
# 开发时间：2023/6/7 15:19
import random
import time

import allure
import pytest

from data_driver.deal_xml import set_xml, set_xml_string
from tools.tools import Tools


def setup_module(module):
    global shg_xscj_path, tools, shg_cd_path
    shg_xscj_path = 'data/DS_1101_SHG_Fix_XSCJ.xml'

    tools = Tools()


@pytest.mark.smoke()
@allure.feature('上交所协商成交')
@allure.title('上交所固定收益平台协商成交委托申报')
@allure.story('正向测试用例')
@allure.severity('blocker')
@allure.issue('http://jira.xquant.com:8888/browse/P015PTJK-2556')
def test_shg_sb_001():
    # 获取当前系统的时间
    long_date, local_date, local_time = tools.get_system_time()
    sysordid = str(int(time.time()))
    # 使用random,生成需要每次不能重复的约定号
    match_no = str(random.randint(100, 999))

    set_xml(shg_xscj_path,
            {'sendDateTime': long_date, 'ordDate': local_date, 'ordTime': local_time, 'matchNo': match_no,
             'sysOrdID': sysordid})
    data = set_xml_string(shg_xscj_path)
    result = tools.send_post(1101, data)
    time.sleep(2)
    with allure.step('数据库断言'):
        sql = f'select t.ordstatus from ttrd_fix_order t  where t.SYSORDID={sysordid}'
        result_list = tools.oracle_link(sql)
        with allure.step('预期结果：ord_status=5'):
            ord_status = result_list[0][0]
        with allure.step(f'实际结果：ord_status={ord_status}'):
            assert ord_status == 5

@pytest.mark.smoke()
@allure.feature('上交所协商成交')
@allure.title('上交所固定收益平台协商成交委托申报')
@allure.story('反向测试用例')
@allure.description('闭市场景的测试')
@allure.severity('blocker')
@allure.issue('http://jira.xquant.com:8888/browse/P015PTJK-2556')
def test_shg_sb_002():
    # 获取当前系统的时间
    long_date, local_date, local_time = tools.get_system_time()
    # 使用时间戳生成唯一的sysordid
    sysordid = str(int(time.time()))
    # 使用random,生成需要每次不能重复的约定号
    match_no = str(random.randint(100, 999))

    set_xml(shg_xscj_path,
            {'sendDateTime': long_date, 'ordDate': local_date, 'ordTime': local_time, 'matchNo': match_no,
             'sysOrdID': sysordid})
    data = set_xml_string(shg_xscj_path)
    result = tools.send_post(1101, data)
    time.sleep(2)
    with allure.step('数据库断言'):
        sql = f'select t.ordstatus,t.errinfo from ttrd_fix_order t  where t.SYSORDID={sysordid}'
        result_list = tools.oracle_link(sql)
        with allure.step('1、预期ord_status结果：ord_status=2'):
            ord_status = result_list[0][0]
            print(result_list[0][1])
            with allure.step(f'实际ord_status结果：ord_status={ord_status}'):
                assert ord_status == 2
        with allure.step('2、预期errinfo结果：errinfo=网络发生故障，与EzDataAccess的通信链路不可用！'):
            errinfo = result_list[0][1]
            with allure.step(f'实际errinfo结果：errinfo={errinfo}'):
                assert errinfo == '网络发生故障，与EzDataAccess的通信链路不可用！'
