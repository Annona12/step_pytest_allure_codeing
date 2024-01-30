# 开发者：Annona
# 开发时间：2024/1/29 11:18
# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2024/1/27 21:17
import sys
from time import sleep


def start_brush(self):
    """买票功能实现"""
    # 浏览器窗口最大化
    self.driver.driver.maximize_window()
    # 登陆
    self.do_login()
    # 跳转到抢票页面
    self.driver.visit(self.ticket_url)
    try:
        print('开始刷票……')
        # 加载车票查询信息
        self.driver.cookies.add({"_jc_save_fromStation": self.from_station})
        self.driver.cookies.add({"_jc_save_toStation": self.to_station})
        self.driver.cookies.add({"_jc_save_fromDate": self.from_time})
        self.driver.reload()
        count = 0
        while self.driver.url == self.ticket_url:
            try:
                self.driver.find_by_text('查询').click()
            except Exception as error_info:
                print(error_info)
                sleep(1)
                continue
            sleep(0.2)
            count += 1
            local_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('第%d次点击查询……[%s]' % (count, local_date))
            try:
                current_tr = self.driver.find_by_xpath(
                    '//tr[@datatran="' + self.number + '"]/preceding-sibling::tr[1]')
                if current_tr:
                    if current_tr.find_by_tag('td')[self.seat_type_index].text == '--':
                        print('无此座位类型出售，已结束当前刷票，请重新开启！')
                        sys.exit(1)
                    elif current_tr.find_by_tag('td')[self.seat_type_index].text == '无':
                        print('无票，继续尝试……')
                        sleep(1)
                    else:
                        # 有票，尝试预订
                        print('刷到票了（余票数：' + str(
                            current_tr.find_by_tag('td')[self.seat_type_index].text) + '），开始尝试预订……')
                        current_tr.find_by_css('td.no-br>a')[0].click()
                        sleep(1)
                        key_value = 1
                        for p in self.passengers:
                            if '()' in p:
                                p = p[:-1] + '学生' + p[-1:]
                            # 选择用户
                            print('开始选择用户……')
                            self.driver.find_by_text(p).last.click()
                            # 选择座位类型
                            print('开始选择席别……')
                            if self.seat_type_value != 0:
                                self.driver.find_by_xpath(
                                    "//select[@id='seatType_" + str(key_value) + "']/option[@value='" + str(
                                        self.seat_type_value) + "']").first.click()
                            key_value += 1
                            sleep(0.2)
                            if p[-1] == ')':
                                self.driver.find_by_id('dialog_xsertcj_ok').click()
                        print('正在提交订单……')
                        self.driver.find_by_id('submitOrder_id').click()
                        sleep(2)
                        # 查看放回结果是否正常
                        submit_false_info = self.driver.find_by_id('orderResultInfo_id')[0].text
                        if submit_false_info != '':
                            print(submit_false_info)
                            self.driver.find_by_id('qr_closeTranforDialog_id').click()
                            sleep(0.2)
                            self.driver.find_by_id('preStep_id').click()
                            sleep(0.3)
                            continue
                        print('正在确认订单……')
                        self.driver.find_by_id('qr_submit_id').click()
                        print('预订成功，请及时前往支付……')
                        # 发送通知信息
                        self.send_mail(self.receiver_email, '恭喜您，抢到票了，请及时前往12306支付订单！')
                        self.send_sms(self.receiver_mobile, '您的验证码是：1230。请不要把验证码泄露给其他人。')
                else:
                    print('不存在当前车次【%s】，已结束当前刷票，请重新开启！' % self.number)
                    sys.exit(1)
            except Exception as error_info:
                print(error_info)
                # 跳转到抢票页面
                self.driver.visit(self.ticket_url)
    except Exception as error_info:
        print(error_info)


def send_sms(self, mobile, sms_info):
    """发送手机通知短信，用的是-互亿无线-的测试短信"""
    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/sms.php?method=Submit"
    account = "C59782899"
    pass_word = "19d4d9c0796532c7328e8b82e2812655"
    params = parse.urlencode(
        {'account': account, 'password': pass_word, 'content': sms_info, 'mobile': mobile, 'format': 'json'}
    )
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib2.HTTPConnectionWithTimeout(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def send_mail(self, receiver_address, content):
    """发送邮件通知"""
    # 连接邮箱服务器信息
    host = 'smtp.163.com'
    port = 25
    sender = 'gxcuizy@163.com'  # 你的发件邮箱号码
    pwd = '******'  # 不是登陆密码，是客户端授权密码
    # 发件信息
    receiver = receiver_address
    body = '<h2>温馨提醒：</h2><p>' + content + '</p>'
    msg = MIMEText(body, 'html', _charset="utf-8")
    msg['subject'] = '抢票成功通知！'
    msg['from'] = sender
    msg['to'] = receiver
    s = smtplib.SMTP(host, port)
    # 开始登陆邮箱，并发送邮件
    s.login(sender, pwd)
    s.sendmail(sender, receiver, msg.as_string())


