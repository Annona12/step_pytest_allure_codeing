# 开发者：Annona
# 开发时间：2023/6/5 14:41
import logging
import time

import allure
import cx_Oracle
from suds.client import Client

from VAR.VAR import *


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
    # def set_dict_value(self,key):


    def test_log(self):
        # 创建日志器
        logger = logging.getLogger()
        # 设置日志级别
        logger.setLevel(logging.INFO)
        # 判断如果没有定义过日志处理器，则进入下面的逻辑
        if not logger.handlers:
            # 指定日志信息显示在哪里 哪个控件
            fh = logging.FileHandler('log.txt', encoding='utf-8')
            logger.addHandler(fh)
            # 设置日志文件的格式
            fhfmt = '%(asctime)s -%(filename)s[line:%(lineno)d] -%(levelname)s: %(message)s'
            shfmtSH = logging.Formatter(fhfmt)
            fh.setFormatter(shfmtSH)
        return logger

# tools = Tools()
# all_val ={"sysOrdID":"1687246771"}
# # # # date = 2023-06-07
# sql = f'select t.ordstatus from ttrd_fix_order t  where t.sysordid={all_val["sysOrdID"]}';
#
# # # print(sql)
# result_list = tools.oracle_link(sql)
# print(result_list[0][0])
# # print(tools.get_system_time()[1])