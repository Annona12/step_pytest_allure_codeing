# 开发者：Annona
# 开发时间：2023/6/5 14:42

# 可以指定只在自动化项目开始运行之前执行一下初始化
import random
import time

import allure
import pytest

from Test.step_allure_auto.data_driver.deal_xml import set_xml, set_xml_string
from Test.step_allure_auto.tools.tools import Tools


@allure.story('正常场景')
@allure.step('前置函数')
@pytest.fixture(scope='session')
def shg_xscj_sb():
    global shg_xscj_path, tools, shg_cd_path
    shg_xscj_path = 'data/DS_1101_SHG_Fix_XSCJ.xml'
    tools = Tools()
    # 获取当前系统的时间
    long_date, local_date, local_time = tools.get_system_time()
    sysordid = str(int(time.time()))
    # 使用random,生成需要每次不能重复的约定号
    match_no = str(random.randint(100, 999))

    set_xml(shg_xscj_path,
            {'sendDateTime': long_date, 'ordDate': local_date, 'ordTime': local_time, 'matchNo': match_no,
             'sysOrdID': sysordid})
    data = set_xml_string(shg_xscj_path)
    print(data)
    result = tools.send_post(1101, data)
    time.sleep(2)
    return tools, sysordid, match_no
    with allure.step('数据库断言'):
        sql = f'select t.ordstatus from ttrd_fix_order t  where t.SYSORDID={sysordid}'
        result_list = tools.oracle_link(sql)
        with allure.step('预期结果：ord_status=5'):
            ord_status = result_list[0][0]
        with allure.step(f'实际结果：ord_status={ord_status}'):
            assert ord_status == 5
            return tools,sysordid,match_no