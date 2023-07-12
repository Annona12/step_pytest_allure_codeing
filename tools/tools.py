# 开发者：Annona
# 开发时间：2023/6/5 14:41
import logging
import time

import allure
import cx_Oracle
from suds.client import Client

from constant.constant import *


class Tools:
    @allure.step('发送webservice请求')
    def send_post(self, action, data):
        cli = Client(URL, headers=HEADERS, faults=False, timeout=15)
        logging.info('发送webservice请求')
        result = cli.service.RequestMessage(action, data)
        return result

    @allure.step('连接数据查询')
    def oracle_link(self, sql):
        conn = cx_Oracle.connect('xir_trd', 'xpar', '191.168.0.213:1521/orcl1')
        cursor = conn.cursor()
        all = cursor.execute(sql)
        # 返回元组形式的查询结果
        result_list = all.fetchall()
        # 循环获取查询的结果的每一组数据
        for i in result_list:
            # 将数据转换成list
            result_list_i = list(i)
            # 获取表字段的详情，包括字段名字、长度、属性等信息
            des = cursor.description
            # 将所有的字段名用.连接成一个字符串存储
            all_field_str = ",".join(item[0] for item in des)
            # 将字段名字使用","分开存储在list中
            field_key = all_field_str.split(',')
            # 设置成字典模式
            dic_result = dict(zip(field_key, result_list_i))
            last_dict_result = []
            last_dict_result.append(dic_result)
        conn.close()
        return last_dict_result[0]

    # 自定义日志处理器
    def my_logger(self):
        now_date = time.strftime("%Y_%m_%d", time.localtime())
        # 日志器，创建日志器
        logger = logging.getLogger()
        # 设置日志级别
        logger.setLevel(logging.INFO)
        # 判断如果没有定义过日志处理器，则进入到下面的逻辑
        # if not logger.handlers:
        # 指定日志信息显示在哪里 哪个组件 控制台  文本文件  处理器
        # 把日志显示到文本
        # 创建文本处理器  文件放在哪  文件地址
        fh = logging.FileHandler(f'../logs/log_{now_date}.txt', encoding='utf-8',mode ='a')
        logger.addHandler(fh)

        # 缺少哪个步骤  格式
        # 格式器  创建格式器  设置自定义格式
        fhfmt = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s_%(funcName)s:%(message)s'
        fhfmtFH = logging.Formatter(fhfmt)
        fh.setFormatter(fhfmtFH)
        return logger
    # 定义获取系统时间的方法，分别返回我们需要的不同规格的时间
    def get_system_time(self):
        long_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        local_date = time.strftime("%Y-%m-%d", time.localtime())
        local_time = time.strftime("%H:%M:%S", time.localtime())
        return long_date, local_date, local_time


# tools = Tools()
# tools.my_logger().info('info信息')
# tools.my_logger().error('error信息')
# # # # date = 2023-06-07
# sql = 'select t.init_date from ttrd_fix_setfl t'
# #
# # # # print(sql)
# result_list = tools.oracle_link(sql)
# print(result_list)
# # print(tools.get_system_time()[1])
