from configparser import ConfigParser
from os import stat
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import warnings
import sys
import multiprocessing as mp
from env_check import *
from page_func import *
from notice import *

warnings.filterwarnings('ignore')


def sys_path(browser):
    path = f'./{browser}/bin/'
    if sys.platform.startswith('win'):
        return path + f'{browser}.exe'
    elif sys.platform.startswith('linux'):
        return path + f'{browser}-linux'
    elif sys.platform.startswith('darwin'):
        return path + f'{browser}'
    else:
        raise Exception('暂不支持该系统')


def load_config(config):
    conf = ConfigParser()
    conf.read(config, encoding='utf8')

    user_name = conf['login']['user_name']
    password = conf['login']['password']
    venue = conf['type']['venue']
    start_time = conf['time']['start_time']
    end_time = conf['time']['end_time']
    wechat_notice = conf.getboolean('wechat', 'wechat_notice')
    sckey = conf['wechat']['SCKEY']

    return (user_name, password, venue, start_time, end_time, wechat_notice, sckey)


def page(config):
    user_name, password, venue, start_time, end_time, wechat_notice, sckey = load_config(
        config)

    log_str = ""
    status = True
    start_time_list_new, end_time_list_new, delta_day_list, log_exceeds = judge_exceeds_days_limit(
        start_time, end_time)
    log_str += log_exceeds
    if len(start_time_list_new) == 0:
        log_status(config, [start_time.split('/'),
                   end_time.split('/')], log_exceeds)
        return False
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        options=chrome_options,
        executable_path=sys_path(browser="chromedriver"),
        service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    print('Driver Launched\n')

    try:
        log_str += login(driver, user_name, password, retry=0)
    except:
        log_str += "登录失败\n"
    try:
        log_str += go_to_venue(driver, venue)
    except:
        log_str += "进入预约 %s 界面失败\n" % venue
    status_book, log_book = book(driver, start_time_list_new,
                                 end_time_list_new, delta_day_list)
    log_str += log_book

    if status_book:
        try:
            log_str += click_agree(driver)
        except:
            log_str += "点击同意失败\n"
            print("点击同意失败\n")
            status = False
        if status:
            try:
                log_str += click_book(driver)
            except:
                log_str += "确定预约失败\n"
                print("确定预约失败\n")
                status = False
        if status:
            try:
                log_str += click_submit_order(driver)
            except:
                log_str += "提交订单失败\n"
                print("提交订单失败\n")
                status = False
        if status:
            try:
                log_str += click_pay(driver)
            except:
                log_str += "付款失败\n"
                print("付款失败\n")
                status = False
        if status and wechat_notice:
            try:
                log_str += wechat_notification(user_name, venue, sckey)
            except:
                log_str += "微信通知失败\n"
                print("微信通知失败\n")
    else:
        status = False
    driver.quit()
    log_status(config, [start_time_list_new, end_time_list_new], log_str)
    return status


def sequence_run(lst_conf):
    print("按序预约")
    for config in lst_conf:
        print("预约 %s" % config)
        page(config)


def multi_run(lst_conf):
    print("并行预约")
    pool = mp.Pool()
    pool.map_async(page, lst_conf)
    pool.close()
    pool.join()


if __name__ == '__main__':
    lst_conf = env_check()
    print(lst_conf)
    print('读取到%d份配置文件\n' % len(lst_conf))

    multi_run(lst_conf)
    # sequence_run(lst_conf)
