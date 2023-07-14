# 开发者：Annona
# 开发时间：2023/6/25 15:46
# 开发者：Annona
# 开发时间：2023/6/5 17:01

# 项目WSDL地址
URL = 'http://191.168.0.212:8913/FixedIncomeService/services/FixedIncomeService?wsdl'

# 项目共用请求头
HEADERS = {
    'Content-Type': 'text/xml',
    'Accept-Charset': 'charset=utf-8'
}

# 项目的测试用例xlsx地址,该地址是相对于mian.py文件的相对地址
EXCEL_PATH_LIST = ['../data/step_case_shg.xlsx']

# 自动化程序日志地址
LOG_PATH = '../logs'

# Step程序的上交所固收通道的交易员
TRADER = 'Z31608'
OB_TRADER = 'Z31605'
