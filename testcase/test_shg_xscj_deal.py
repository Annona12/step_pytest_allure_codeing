# 开发者：Annona
# 开发时间：2023/6/16 14:22
import time

import allure
import pytest

from Test.step_allure_auto.data_driver.deal_xml import set_xml, set_xml_string


def setup_module(module):
    global shg_xscj_path, shg_cd_path
    shg_xscj_path = 'data/DS_1101_SHG_Fix_XSCJ.xml'


# @pytest.mark.smoke()
@allure.feature('上交所协商成交')
@allure.story('正向测试用例')
@allure.title('上交所固定收益平台协商成交成交测试')
def test_shg_xscj_deal_001(shg_xscj_sb):
    tools, sysordid_shg, match_no = shg_xscj_sb
    # 获取当前系统的时间
    long_date, local_date, local_time = tools.get_system_time()
    sysordid = str(int(time.time()))
    sql = f'select * from ttrd_fix_order t  where t.SYSORDID={sysordid_shg}'
    result_list = tools.oracle_link(sql)
    print(result_list)
    if result_list[0][7] == 'S':
        print(result_list[0][22],result_list[0][23])
        set_xml(shg_xscj_path,
            {'sendDateTime': long_date, 'ordDate': local_date, 'ordTime': local_time, 'matchNo': match_no,
             'sysOrdID': sysordid,'dir':'B','bOrdCount':str(result_list[0][22]),'bOrdPrice':str(result_list[0][23]),'sOrdCount':'0','sOrdPrice':'0',
             'trader':result_list[0][14],'obTrader':result_list[0][9]})
    elif result_list[0][7] == 'B':
        set_xml(shg_xscj_path,
            {'sendDateTime': long_date, 'ordDate': local_date, 'ordTime': local_time, 'matchNo': match_no,
             'sysOrdID': sysordid,'dir':'S','bOrdCount':'0','bOrdPrice':'0','sOrdCount':str(result_list[0][20]),'sOrdPrice':str(result_list[0][21]),
             'trader':result_list[0][14],'obTrader':result_list[0][9]})
    else:
        print('输入的方向错误，请检查！！！')

    data = set_xml_string(shg_xscj_path)
    print(data)
    # result = tools.send_post(1101, data)
    # print(result)
    # print(data)
