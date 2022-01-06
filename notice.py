from email.header import Header
from email.mime.text import MIMEText
from urllib.parse import quote
from urllib import request
import json


def wechat_notification(user_name, venue, filed_num, start_time, end_time, sckey):
    with request.urlopen(
            quote('https://sctapi.ftqq.com/' + sckey + '.send?title=成功预约&desp=学号：' +
                  str(user_name) + ' 成功预约：' + str(venue) + " 场地编号："+str(filed_num) +
                  " 开始时间："+str(start_time)+" 结束时间："+str(end_time),
                  safe='/:?=&')) as response:
        response = json.loads(response.read().decode('utf-8'))
        if response['code'] == 0 and response['data']['error'] == 'SUCCESS':
            print('微信通知成功')
        else:
            print(str(response['errno']) + ' error: ' + response['errmsg'])
    return "微信通知成功\n"


if __name__ == '__main__':
    wechat_notification('', "羽毛球场测试",
                        "")
