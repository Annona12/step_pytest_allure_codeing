import requests
import json
import time
import re
import urllib.parse
import webbrowser


def login():
    session = requests.Session()
    session.get('https://kyfw.12306.cn/otn/login/init')
    login_url = 'https://kyfw.12306.cn/passport/web/login'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://kyfw.12306.cn/otn/login/init',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    data = {
        'username': '',
        'password': '',
        'appid': 'otn'
    }
    response = session.post(login_url, headers=headers, data=data)
    print(response.cookies)
    if response.status_code == 200:
        print('登录成功')
        return session
    else:
        print('登录失败')
        return None


def query_tickets(session, from_station, to_station, date, purpose_codes):
    query_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    params = {
        'leftTicketDTO.train_date': date,
        'leftTicketDTO.from_station': from_station,
        'leftTicketDTO.to_station': to_station,
        'purpose_codes': purpose_codes
    }
    response = session.get(query_url, headers=headers, params=params)
    if response.status_code == 200:
        result = json.loads(response.text)
        if result['status'] and result['status'] == True:
            tickets = result['data']['result']
            for ticket in tickets:
                ticket_info = ticket.split('|')
                train_no = ticket_info[3]
                from_station_name = ticket_info[6]
                to_station_name = ticket_info[7]
                start_time = ticket_info[8]
                arrive_time = ticket_info[9]
                duration = ticket_info[10]
                swz_num = ticket_info[32] or '--'
                tz_num = ticket_info[25] or '--'
                zy_num = ticket_info[31] or '--'
                ze_num = ticket_info[30] or '--'
                gr_num = ticket_info[21] or '--'
                rw_num = ticket_info[23] or '--'
                yw_num = ticket_info[28] or '--'
                rz_num = ticket_info[24] or '--'
                yz_num = ticket_info[29] or '--'
                wz_num = ticket_info[26] or '--'
                print(train_no, from_station_name, to_station_name, start_time, arrive_time, duration, swz_num, tz_num,
                      zy_num, ze_num, gr_num, rw_num, yw_num, rz_num, yz_num, wz_num)
        else:
            print('查询车票信息失败')
    else:
        print('查询车票信息失败')


def submit_order(session, train_no, from_station, to_station, date, purpose_codes, seat_type):
    submit_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    data = {
        'secretStr': urllib.parse.unquote(secret_str),
        'train_date': date,
        'back_train_date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
        'tour_flag': 'dc',
        'purpose_codes': purpose_codes,
        'query_from_station_name': from_station,
        'query_to_station_name': to_station,
        'undefined': ''
    }
    response = session.post(submit_url, headers=headers, data=data)
    if response.status_code == 200:
        result = json.loads(response.text)
        if result['status'] and result['status'] == True:
            print('提交订单成功')
            return result['data']
        else:
            print('提交订单失败')
            return None
    else:
        print('提交订单失败')
        return None


def confirm_order(session, passenger_name, passenger_id, old_passenger_id, seat_type, train_no, from_station,
                  to_station, date, train_location, repeat_submit_token):
    confirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    data = {
        'passengerTicketStr': '{},0,1,{},N,{},,{},N'.format(seat_type, passenger_name, passenger_id, old_passenger_id),
        'oldPassengerStr': '{},1,{},3_'.format(passenger_name, passenger_id),
        'randCode': '',
        'purpose_codes': '00',
        'key_check_isChange': key_check_is_change,
        'leftTicketStr': urllib.parse.unquote(left_ticket_str),
        'train_location': train_location,
        'choose_seats': '',
        'seatDetailType': '000',
        'whatsSelect': '1',
        'roomType': '00',
        'dwAll': 'N',
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': repeat_submit_token
    }
    response = session.post(confirm_url, headers=headers, data=data)
    if response.status_code == 200:
        result = json.loads(response.text)
        if result['status'] and result['status'] == True:
            print('确认订单成功')
            return result['data']['payurl']
        else:
            print('确认订单失败')
            return None
    else:
        print('确认订单失败')
        return None


def pay(pay_url):
    webbrowser.open(pay_url)


if __name__ == '__main__':
    session = login()
    # query_tickets(session, 'HZH', 'DCG', '2024-02-01', 'ADULT')
    # submit_order(session, 'G101', 'BJP', 'SHH', '2022-01-01', 'ADULT', 'O')
    # confirm_order(session, '张三', '123456789012345678', '1_1_1', 'O', 'G101', 'BJP', 'SHH', '2022-01-01', 'N',
    #               '1234567890abcdefg')
    # pay('https://pay.12306.cn/pay/payGateway.html')
