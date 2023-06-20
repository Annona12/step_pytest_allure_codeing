# 开发者：Annona
# 开发时间：2023/6/19 14:46
# 开发者：Annona
# 开发时间：2023/6/16 17:36
import openpyxl


def read_excel(excel_path):
    excel = openpyxl.load_workbook(excel_path)
    sheet = excel.active
    case_list = []
    for item in sheet.values:
        if type(item[0]) is int:
            case_list.append(item)
    return case_list

# print(read_excel('../data/step_case.xlsx'))