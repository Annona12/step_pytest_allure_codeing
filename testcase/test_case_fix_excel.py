# # 开发者：Annona
# # 开发时间：2023/6/19 14:50
# import logging
# import time
# import allure
# import openpyxl
# import pytest
#
# from constant.constant import EXCEL_PATH
# from data_driver.deal_excel import read_excel
# from data_driver.deal_xml import set_xml, set_xml_string
# from tools.tools import Tools
#
#
# # set_module在当前文件中，在所有测试用例执行之前执行
# def setup_module(module):
#     # 定义全局变量，当前文件的函数都可以访问
#     global tools, all_val, excel, excel_path
#     # 实例化工具类
#     tools = Tools()
#     excel_path = EXCEL_PATH
#     excel = openpyxl.load_workbook(excel_path)
#     sheet_names = excel.sheetnames
#     # 参数化变量存储字典，临时存储sysOrdID或者machNo字典值
#     all_val = {}
#
#
# @pytest.mark.parametrize('data',read_excel())
# def test_shg_fix(data):
#     logging.info(data)
#     if data[12] == 'no':
#         pytest.skip("标记该用例为不执行")
#     # 动态生成测试用例的feature(一个feature代表一个sheet页)、story(一个story一个业务)、
#     # title(测试用例名称)、description、severity
#     if data[-1] is not None:
#         allure.dynamic.feature(data[-1])
#     if data[1] is not None:
#         allure.dynamic.story(data[1])
#     if data[2] is not None:
#         allure.dynamic.title(data[2])
#     if data[3] is not None:
#         allure.dynamic.description(data[3])
#     if data[4] is not None:
#         allure.dynamic.severity(data[4])
#
#     # 获取当前sheet页的名字和所在行数
#     sheet_active = data[-1]
#     sheet = excel[sheet_active]
#     row_num = data[0] + 1
#
#     # 将从excel中读取的数据放入参数中
#     # 获取功能号单元格的数据数据
#     action_str = str(data[5])
#     # 获取需要读取的xml文件数据
#     xml_str = data[6]
#     # 获取需要重新设置的参数数据
#     param_str = data[7]
#     # 各个数据分别使用“;”分开，获取list
#     act_list = action_str.split(';')
#     xml_list = xml_str.split(';')
#     param_list = param_str.split(';')
#
#     # 判断用例中传递的功能号、读取报文地址、修改参数个数是否对应正确
#     if len(act_list) == len(xml_list) == len(param_list):
#         # 用来标志下面的代码是否需要运行：
#         flag = True
#         # 对于每一行action有多个数据时，循环发送请求
#         for i in range(len(act_list)):
#             # 获取当前系统的时间
#             long_date, local_date, local_time = tools.get_system_time()
#             # 使用random,生成需要每次不能重复的约定号
#             # 当前请求的参数设置
#             try:
#                 # 将修改参数转换成字典格式
#                 param_list_i = eval(param_list[i])
#                 # 将系统时间等信息设置到xml报文中,申报类的报文，默认将这些都添加到参数中
#                 param_list_i['sendDateTime'] = long_date
#                 param_list_i['ordDate'] = local_date
#                 param_list_i['ordTime'] = local_time
#                 param_list_i['actDate'] = local_date
#                 param_list_i['actTime'] = local_time
#                 param_list_i['orgOrdDate'] = local_date
#
#                 # 按照时间戳生成主键sysOrdID，并将该值存储在all_val，以便后续查询数字库，做断言使用
#                 if 'sysOrdID' in param_list_i.keys():
#                     sysord_id = str(int(time.time()))
#                     param_list_i['sysOrdID'] = sysord_id
#                     all_val['sysOrdID'] = sysord_id
#                 # if 'matchNo' in param_list_i.keys():
#                 #     match_no = str(random.randint(100, 999))
#                 #     param_list_i['matchNo'] = match_no
#                 #     all_val['matchNo'] = match_no
#                 # 如果参数中有orgSysOrdID字段，则需要取出all_val中的sysOrdID值，对该笔报价进行撤单
#                 if 'orgSysOrdID' in param_list_i.keys():
#                     param_list_i['orgSysOrdID'] = all_val['sysOrdID']
#                 # 获取了所有最新的需要修改的参数之后，调用工具函数将各个参数写入xml文件中
#                 set_xml(xml_list[i], param_list_i)
#                 data_xml = set_xml_string('data/temp.xml')
#                 logging.info(data_xml)
#                 # 发送请求
#                 result = tools.send_post(act_list[i], data_xml)
#                 logging.info(result)
#                 time.sleep(5)
#             except:
#                 print('修改参数转换成字典格式错误，请检查修改参数列数据！！！')
#                 sheet.cell(row_num, 12).value = '修改参数转换成字典格式错误，请检查修改参数列数据！！！'
#                 flag = False
#                 assert 0 == 1
#         if flag :
#             if data[8] is not None and data[9] is not None and data[10] is not None:
#                 # 查询数据库的基础sql
#                 sql_str = data[8]
#                 sql_str_list = sql_str.split(';')
#                 # 获取预期结果的内容
#                 hope_result = data[10]
#                 hope_result_list = hope_result.split(';')
#                 hope_result_dic_list = []
#                 # 数据库变量
#                 sql_param_str = data[9]
#                 # 将数据库变量用";"分隔
#                 sql_param_list = sql_param_str.split(';')
#                 # 存储经过转换后的数据库变量
#                 param_list_num = []
#                 # 获取列表长度
#                 length = len(sql_param_list)
#                 # 循环解析all_val[]值并填入list1
#                 for j in range(length):
#                     flag=True
#                     try:
#                         param_list_num.append(eval(sql_param_list[j]))
#                     except:
#                         print('数据库变量转换失败，请检查数据库变量列的数据！！！')
#                         sheet.cell(row_num, 12).value = '数据库变量转换失败，请检查数据库变量列的数据！！！'
#                         flag = False
#                         assert 0 == 1
#                 if flag:
#                     try:
#                         for item in hope_result_list:
#                             temp_item = eval(item)
#                             hope_result_dic_list.append(temp_item)
#                     except:
#                         print('预期结果值转换成字典格式失败，请检查预期结果列数据！！！')
#                         sheet.cell(row_num, 12).value = '预期结果值转换成字典格式失败，请检查预期结果列数据！！！'
#                         flag = False
#                         assert 0 == 1
#                     if flag:
#                         if len(hope_result_dic_list) == len(sql_str_list):
#                             for i in range(len(sql_str_list)):
#                                 flag = True
#                                 try:
#                                     sql = sql_str_list[i].format(*param_list_num)
#                                     logging.info(sql)
#                                     result_list = tools.oracle_link(sql)
#                                 except:
#                                     sheet.cell(row_num, 12).value = 'sql语句有误，请检查！！！'
#                                     logging.info('sql语句有误，请检查！！！')
#                                     flag = False
#                                     assert 0 == 1
#                                 if flag:
#
#                                     for key in hope_result_dic_list[i].keys():
#                                         real_result = result_list[key]
#                                         if real_result == hope_result_dic_list[i][key]:
#                                             sheet.cell(row_num, 12).value = '测试通过'
#                                         else:
#                                             print('测试不通过')
#                                             sheet.cell(row_num, 12).value = '测试不通过'
#                                     for key in hope_result_dic_list[i].keys():
#                                         with allure.step(f"数据库{key}断言"):
#                                             with allure.step(f'预期结果：{key}={hope_result_dic_list[i][key]}'):
#                                                 real_result = result_list[key]
#                                             with allure.step(f'实际结果：{key}={real_result}'):
#                                                 assert real_result == hope_result_dic_list[i][key]
#                                 else:
#                                     pass
#                         else:
#                             print('查询sql与预期结果字典个数不对应，请检查！！！')
#                             sheet.cell(row_num, 12).value = '查询sql与预期结果字典个数不对应，请检查！！！'
#                             assert 0 == 1
#                     else:
#                         pass
#                 else:
#                     pass
#             else:
#                 sheet.cell(row_num, 12).value = "查询数据库sql或者预期结果确实，请检查！！！"
#                 logging.info('查询数据库sql或者预期结果或者数据变量缺失，请检查！！！')
#                 assert 0 ==1
#         else:
#             pass
#     else:
#         sheet.cell(row_num, 12).value = "用例中传递的功能号、读取报文地址、修改参数个数不对应请检查！！！"
#         logging.error('用例中传递的功能号、读取报文地址、修改参数个数不正确请检查！！！')
#         assert 0 == 1
#     excel.save(excel_path)
#
