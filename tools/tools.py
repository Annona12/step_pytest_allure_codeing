# 开发者：Annona
# 开发时间：2023/6/5 14:41
import time

import allure
import cx_Oracle
from suds.client import Client

from Test.step_allure_auto.VAR.VAR import *


class Tools:
    @allure.step('发送请求')
    def send_post(self,action,data):
        cli = Client(URL, headers=HEADERS, faults=False, timeout=15)
        result = cli.service.RequestMessage(action, data)
        return result
    @allure.step('连接数据库查询')
    def oracle_link(self, sql):
        conn = cx_Oracle.connect('xir_trd', 'xpar', '191.168.0.213:1521/orcl')
        cursor = conn.cursor()
        all = cursor.execute(sql)
        result_list = all.fetchall()
        conn.close()
        return result_list
    # 定义获取系统时间的方法，分别返回我们需要的不同规格的时间
    def get_system_time(self):
        long_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        local_date = time.strftime("%Y-%m-%d", time.localtime())
        local_time = time.strftime("%H:%M:%S", time.localtime())
        return long_date,local_date,local_time

# tools = Tools()
# # date = 2023-06-07
# sql = 'select t.sysordid,t.ordstatus from ttrd_fix_order t  where t.orddate={}'.format("'2023-06-07'")
# print(sql)

# result_list = tools.oracle_link(sql)
# print(result_list)