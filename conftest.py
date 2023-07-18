# 开发者：Annona
# 开发时间：2023/6/5 14:42
import logging
import random
import time

import allure
import pytest

from constant.constant import *
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
    MY_LOGGER.info('前置函数，交易初始化！')
    global tools
    tools = Tools()
    long_date, local_date, local_time = tools.get_system_time()
    sql = 'select t.init_date from ttrd_fix_setflag t'
    MY_LOGGER.info(sql)
    try:
        tools.conn_oracle(
            dsn=ORACLE_DSN,
            user=ORACLE_USER,
            passwd=ORACLE_PASSWORD
        )
        result = tools.sql_check(sql)
        MY_LOGGER.info(result)
    except:
        MY_LOGGER.error('数据库查询失败')
    finally:
        tools.close_connection()
    if result['INIT_DATE'] == local_date:
        MY_LOGGER.info('初始化日期[2023-07-10]等于已初始化日期[2023-07-10]，不允许重复初始化')
    else:
        send_init_request(long_date, local_date)

def send_init_request(long_date, local_date):
    MY_LOGGER.info(f"sendDateTime: {long_date}, initDate: {local_date}")
    step_init = 'data/shg_fix/DS_1100_STEP_INIT.xml'
    set_xml(step_init, {'sendDateTime': long_date, 'initDate': local_date})
    data = set_xml_string('data/temp.xml')
    MY_LOGGER.info(data)
    result = tools.send_post(1100, data)
    MY_LOGGER.info(result)


