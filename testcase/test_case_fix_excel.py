# 开发者：Annona
# 开发时间：2023/6/19 14:50
import random
import time

import allure
import openpyxl
import pytest

from data_driver.deal_excel import read_excel
from data_driver.deal_xml import set_xml, set_xml_string
from tools.tools import Tools


def setup_module(module):
    # 定义全局变量，当前文件的函数都可以访问
    global tools, all_val
    # 实例化工具类
    tools = Tools()
    # 参数化变量存储字典，临时存储sysOrdID或者machNo字典值
    all_val = {}


@pytest.mark.parametrize('data', read_excel('data/step_case.xlsx'))
def test_shg_fix_xscj(data):
    # 动态生成测试用例的feature、story、title、description、severity
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

    # 将从excel中读取的数据放入参数中
    # 获取功能号单元格的数据数据
    action_str = str(data[6])
    # 获取需要读取的xml文件数据
    xml_str = data[7]
    # 获取需要重新设置的参数数据
    param_str = data[8]
    # 各个数据分别使用“;”分开，获取list
    act_list = action_str.split(';')
    xml_list = xml_str.split(';')
    param_list = param_str.split(';')
    # 对于每一行action有多个数据时，循环发送请求
    for i in range(len(act_list)):
        # 获取当前系统的时间
        long_date, local_date, local_time = tools.get_system_time()
        # 当前请求的参数设置
        param_list_i = eval(param_list[i])

        # 将系统时间等信息设置到xml报文中,申报类的报文，默认将这些都添加到参数中
        param_list_i['sendDateTime'] = long_date
        param_list_i['ordDate'] = local_date
        param_list_i['ordTime'] = local_time
        param_list_i['actDate'] = local_date
        param_list_i['actTime'] = local_time
        param_list_i['orgOrdDate'] = local_date

        # 按照时间戳生成主键sysOrdID，并将该值存储在all_val，以便后续查询数字库，做断言使用
        if 'sysOrdID' in param_list_i.keys():
            sysord_id = str(int(time.time()))
            param_list_i['sysOrdID'] = sysord_id
            all_val['sysOrdID'] = sysord_id

        # 如果参数中有orgSysOrdID字段，则需要取出all_val中的sysOrdID值，对该笔报价进行撤单
        if 'orgSysOrdID' in param_list_i.keys():
            param_list_i['orgSysOrdID'] = all_val['sysOrdID']
        # 获取了所有最新的需要修改的参数之后，调用工具函数将各个参数写入xml文件中
        set_xml(xml_list[i], param_list_i)
        data_xml = set_xml_string(xml_list[i])
        # 发送请求
        result = tools.send_post(act_list[i], data_xml)
        print(data_xml)
        print(result)
        time.sleep(2)

    if data[9] is not None and data[10] is not None and data[11] is not None:
        # 查询数据库的基础sql
        sql_str = data[9]
        sql_str_list = sql_str.split(';')
        for i in range(len(sql_str_list)):
            # 数据库变量
            sql_param_str = data[10]
            # 将数据库变量用";"分隔
            sql_param_list = sql_param_str.split(';')
            # 存储经过转换后的数据库变量
            param_list_num = []
            # 获取列表长度
            length = len(sql_param_list)
            # 循环解析all_val[]值并填入list1
            for j in range(length):
                param_list_num.append(eval(sql_param_list[j]))
            sql = sql_str_list[i].format(*param_list_num)
            print(sql)
            hope_result = data[11]
            hope_result_dic = eval(hope_result)
            result_list = tools.oracle_link(sql)
            with allure.step('1、数据库状态断言：'):
                with allure.step(f'预期结果：ord_status={hope_result_dic["ordstatus"]}'):
                    ord_status = result_list[0][0]
                with allure.step(f'实际结果：ord_status={ord_status}'):
                    assert ord_status == hope_result_dic["ordstatus"]
            with allure.step('2、数据库错误信息断言：'):
                with allure.step(f'预期结果：ord_status={hope_result_dic["errinfo"]}'):
                    ord_errinfo = result_list[0][1]
                with allure.step(f'实际结果：ord_status={ord_errinfo}'):
                    assert ord_errinfo == hope_result_dic["errinfo"]
            # print(result_list)
            # print(data[11])
