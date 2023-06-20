# 开发者：Annona
# 开发时间：2023/6/7 15:10
import time

import allure
import pytest

from data_driver.deal_xml import set_xml, set_xml_string


def setup_module(module):
    global shg_xscj_path, shg_cd_path
    shg_xscj_path = 'data/DS_1102_SHG_CD.xml'

@pytest.mark.smoke()
@allure.feature('上交所协商成交')
@allure.title('上交所固定收益平台撤单申报')
@allure.story('正向测试用例')
def test_shg_cd_001(shg_xscj_sb):
    tools, sysordid ,match_no= shg_xscj_sb
    # 获取当前系统的时间
    long_date, local_date, local_time = tools.get_system_time()
    set_xml(shg_xscj_path,
            {'sendDateTime': long_date, 'actDate': local_date, 'actTime': local_time, 'orgOrdDate': local_date,
             'orgSysOrdID': sysordid})
    data = set_xml_string(shg_xscj_path)
    result = tools.send_post(1102, data)
    print(result)
    time.sleep(2)
    with allure.step('数据库断言'):
        sql = f'select t.ordstatus from ttrd_fix_order t  where t.SYSORDID={sysordid}'
        result_list = tools.oracle_link(sql)
        with allure.step('预期结果：ord_status=9'):
            ord_status = result_list[0][0]
        with allure.step(f'实际结果：ord_status={ord_status}'):
            assert ord_status == 9
