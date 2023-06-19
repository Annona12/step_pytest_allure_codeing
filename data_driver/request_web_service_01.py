# 开发者：Annona
# 开发时间：2023/6/2 14:46
from suds.client import Client

from Test.step_allure_auto_coding.data_driver.deal_xml import *

url = 'http://191.168.0.212:8113/FixedIncomeService/services/FixedIncomeService?wsdl'
headers = {
    'Content-Type': 'text/xml',
    'Accept-Charset':'charset=urf-8'
}
cli = Client(url, headers=headers, faults=False, timeout=15)
data = set_xml_string('../data/DS_1101_SHG_Fix_XSCJ.xml')
result = cli.service.RequestMessage(1101,data)

print(type(result))
print(result[0])
print(result)