# 开发者：Annona
# 开发时间：2023/6/19 14:46
# 开发者：Annona
# 开发时间：2023/6/16 17:36
import logging

import openpyxl

from constant.constant import EXCEL_PATH

def read_excel():
    # 加载excel
    excel = openpyxl.load_workbook(EXCEL_PATH)
    # 获取excel中所有的sheet表名
    sheet_names = excel.sheetnames
    all_case_list = []
    for i in range(len(sheet_names)):
        sheet_active = excel[sheet_names[i]]
        for item in sheet_active.values:
            if type(item[0]) is int:
                temp_list = list(item)
                temp_list.append(sheet_names[i])
                all_case_list.append(tuple(temp_list))
    logging.info('完成')
    return all_case_list
