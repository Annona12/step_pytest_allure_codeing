# 开发者：Annona
# 开发时间：2023/6/5 14:41
import datetime
import logging
import time

import allure
import cx_Oracle
import pymysql
from suds.client import Client

from constant.constant import *


class Tools:
    def __init__(self):
        self.connection = None

    @allure.step('发送webservice请求')
    def send_post(self, action, data):
        try:
            cli = Client(URL, headers=HEADERS, faults=False, timeout=15)
            result = cli.service.RequestMessage(action, data)
            MY_LOGGER.info('发送POST请求完成')
            return result
        except Exception as e:
            MY_LOGGER.error('发送POST请求失败,错误信息：')
            MY_LOGGER.error(str(e))
            return None

    def conn_oracle(self, dsn, user, passwd):
        """
        连接oracle数据库
        :param dsn: 数据库的数据源名称，它可以是一个 TNS 格式的连接字符串，或者是一个字典对象.
        :param user: 要连接的数据库用户的用户名
        :param passwd: 要连接的数据库用户的密码
        :return: 返回连接实例
        """
        try:
            self.connection = cx_Oracle.connect(user=user, password=passwd, dsn=dsn)
        except cx_Oracle.Error as e:
            MY_LOGGER.error('连接数据库失败，错误信息：')
            MY_LOGGER.error(e)

    def conn_mysql(self, host, port, user, passwd, database, charset):
        """
        连接mysql数据库
        :param host: ip
        :param port: 端口
        :param user: 用户名
        :param passwd: 密码
        :param database: 数据库实例
        :param charset: 编码格式
        :return: 连接实例
        """
        try:
            self.connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                passwd=passwd,
                database=database,
                charset=charset
            )
        except pymysql.Error as e:
            MY_LOGGER.error('连接数据库失败,错误信息：')
            MY_LOGGER.error(str(e))

    @allure.step('数据库查询')
    def sql_check(self, sql):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            result_list = []
            # 获取每个字段的信息
            des = cursor.description
            for result in results:
                result_dict = {}
                for i in range(len(result)):
                    result_dict[des[i][0]] = result[i]
                result_list.append(result_dict)
            cursor.close()
            return result_list[0]
        except cx_Oracle.Error as e:
            MY_LOGGER.error('执行SQL查询失败，错误信息：')
            MY_LOGGER.error(e)
        except pymysql.Error as e:
            MY_LOGGER.error('执行SQL查询失败,错误信息：')
            MY_LOGGER.error(e)

    def close_connection(self):
        if self.connection:
            self.connection.close()
            MY_LOGGER.info('数据库连接关闭！！！')

    def get_system_time(self):
        long_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        local_date = time.strftime("%Y-%m-%d", time.localtime())
        local_time = time.strftime("%H:%M:%S", time.localtime())
        return long_date, local_date, local_time

