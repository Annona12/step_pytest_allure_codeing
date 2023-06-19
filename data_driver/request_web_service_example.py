# 开发者：Annona
# 开发时间：2023/6/5 10:59
from suds import client

# webservice的地址
url = 'http://ws.webxml.com.cn/WebServices/MobileCodeWS.asmx?wsdl'
# 创建webservice对象
cli = client.Client(url)
# print(cli)  # 查看全部方法

"""
调用service接口
测试调用第一个
获得国内手机号码归属地数据库信息
输入参数：无，返回数据：一堆字符串数组（省份、城市、记录数量）
调用接口的格式：client.service.方法名称(参数)
"""
tels = cli.service.getDatabaseInfo()
# print(tels)


"""
获得国内手机号码归属地省份、地区和手机卡类型信息
输入参数：mobileCode=字符串（手机号码，最少前7位数字）,userID=字符串（商业用户ID）免费用户位空字符串;
返回数据：字符串（手机号码：省份 城市 手机卡类型）

"""
result = cli.service.getMobileCodeInfo(mobileCode='13777550226',userID='')
print(result)
