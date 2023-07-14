# 开发者：Annona
# 开发时间：2023/6/5 14:41
import datetime

import allure
import cx_Oracle
import pymysql
from suds.client import Client

from constant.constant import *
from my_logger import MyLogger


class Tools:
    global my_logger
    my_logger = MyLogger(LOG_PATH)
    def __init__(self):
        self.connection = None

    @allure.step('发送webservice请求')
    def send_post(self, action, data):

        try:
            cli = Client(URL, headers=HEADERS, faults=False, timeout=15)
            result = cli.service.RequestMessage(action, data)
            my_logger.info('发送POST请求完成')
            return result
        except Exception as e:
            my_logger.error('发送POST请求失败,错误信息：')
            my_logger.error(str(e))
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
            my_logger.error('连接数据库失败，错误信息：')
            my_logger.error(e)

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
            my_logger.error('连接数据库失败,错误信息：')
            my_logger.error(e)

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
            return result_list
        except cx_Oracle.Error as e:
            my_logger.error('执行SQL查询失败，错误信息：')
            my_logger.error(e)
        except pymysql.Error as e:
            my_logger.error('执行SQL查询失败,错误信息：')
            my_logger.error(e)

    def close_connection(self):
        if self.connection:
            self.connection.close()
            my_logger.info('数据库连接关闭！！！')


    def get_system_time(self):
        now = datetime.now()
        long_date = now.strftime("%Y-%m-%d %H:%M:%S")
        local_date = now.strftime("%Y-%m-%d")
        local_time = now.strftime("%H:%M:%S")
        return long_date, local_date, local_time

if __name__ == '__main__':
    ky = Tools()
    try:
        ky.conn_oracle(
            dsn='191.168.0.213:1521/orcl1',
            user='xir_trd',
            passwd='xpar'
        )
        requests = ky.sql_check(sql='SELECT t.* FROM TTRD_FIX_PLATFROM_INFO_STATUS t')
        print(requests)
    except:
        print("查询数据库失败")
    finally:
        ky.close_connection()