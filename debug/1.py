# 开发者：Annona
# 开发时间：2024/1/29 10:41
import requests
from lxml import html
import re


# 登录步骤
def login(username, password):
    # 登录URL
    login_url = 'https://kyfw.12306.cn/otn/login/loginAysnSuggest'
    session = requests.session()
    # 获取验证码
    captcha_res = session.get(
        'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&.jpg')
    with open('captcha.jpg', 'wb') as f:
        f.write(captcha_res.content)
    captcha_code = input('请输入验证码：')
    # 登录数据
    login_data = {
        'username': username,
        'password': password,
        'appid': 'otn',
        'use_rd_captcha': 'A',
        'captcha-sid': '...',  # 这里填写从验证码图片里获取的captcha-sid
        'captcha_type': 'login',
        'answer': captcha_code,
    }
    # 登录请求
    session.post(login_url, data=login_data)
    return session


# 购票步骤
def buy_ticket(session, from_station, to_station, train_date):
    # 购票URL
    buy_ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    # 查询车次信息
    # ...
    # 选择车次，座位，和预订
    # ...
    # 订单信息
    order_data = {
        # 订单相关信息
    }
    # 提交订单
    order_response = session.post(buy_ticket_url, data=order_data)
    # 处理订单结果
    # ...


# 主程序
def main():
    # 用户名和密码
    username = 'your_username'
    password = 'your_password'
    # 出发地和目的地
    from_station = 'SHH'
    to_station = 'BJP'
    # 出行日期
    train_date = '2024-02-01'

    # 登录
    session = login(username, password)

    # 购票
    # buy_ticket(session, from_station, to_station, train_date)


if __name__ == '__main__':
    main()