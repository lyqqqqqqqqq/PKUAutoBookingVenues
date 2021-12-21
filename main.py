from configparser import ConfigParser
from os import stat
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Chrome_Options
from selenium.webdriver.firefox.options import Options as Firefox_Options
import warnings
import sys
import multiprocessing as mp
from env_check import *
from page_func import *
from notice import *

warnings.filterwarnings('ignore')


def sys_path(browser):
    path = 'driver'
    if browser == "chrome":
        if sys.platform.startswith('win'):
            return os.path.join(path, 'chromedriver.exe')
        elif sys.platform.startswith('linux'):
            return os.path.join(path, 'chromedriver.bin')
        else:
            raise Exception('不支持该系统')
    elif browser == "firefox":
        if sys.platform.startswith('win'):
            return os.path.join(path, 'geckodriver.exe')
        elif sys.platform.startswith('linux'):
            return os.path.join(path, 'geckodriver.bin')
        else:
            raise Exception('不支持该系统')


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


def log_status(config, start_time, log_str):
    print("记录日志")
    now = datetime.datetime.now()
    print(now)
    print('%s.log' % config.split('.')[0])
    with open('%s.log' % config.split('.')[0], 'a', encoding='utf-8') as fw:
        fw.write(str(now)+"\n")
        fw.write("%s\n" % str(start_time))
        fw.write(log_str+"\n")
    print("记录日志成功\n")


def page(config, browser="chrome"):
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
    if browser == "chrome":
        chrome_options = Chrome_Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(
            options=chrome_options,
            executable_path=sys_path(browser="chrome"))
        print('chrome launched\n')
    elif browser == "firefox":
        firefox_options = Firefox_Options()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(
            options=firefox_options,
            executable_path=sys_path(browser="firefox"))
        print('firefox launched\n')
    else:
        raise Exception("不支持此类浏览器")

    if status:
        try:
            log_str += login(driver, user_name, password, retry=0)
        except:
            log_str += "登录失败\n"
            status = False
    if status:
        status, log_venue = go_to_venue(driver, venue)
        log_str += log_venue
        # try:
        #     status, log_venue = go_to_venue(driver, venue)
        #     log_str += log_venue
        # except:
        #     log_str += "进入预约 %s 界面失败\n" % venue
        #     status = False
    if status:
        status, log_book, start_time, end_time = book(driver, start_time_list_new,
                                                      end_time_list_new, delta_day_list)
        log_str += log_book
    else:
        log_str += "点击预约表格失败\n"
        print("点击预约表格失败\n")
        status = False

    if status:
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
            log_str += wechat_notification(user_name,
                                           venue, start_time, end_time, sckey)
        except:
            log_str += "微信通知失败\n"
            print("微信通知失败\n")
    driver.quit()
    log_status(config, [start_time_list_new, end_time_list_new], log_str)
    return status


def sequence_run(lst_conf, browser="chrome"):
    print("按序预约")
    for config in lst_conf:
        print("预约 %s" % config)
        page(config, browser)


def multi_run(lst_conf, browser="chrome"):
    parameter_list = []
    for i in range(len(lst_conf)):
        parameter_list.append((lst_conf[i], browser))
    print("并行预约")
    pool = mp.Pool()
    pool.starmap_async(page, parameter_list)
    pool.close()
    pool.join()


if __name__ == '__main__':
    browser = "firefox"

    lst_conf = env_check()
    print(lst_conf)
    print('读取到%d份配置文件\n' % len(lst_conf))

    multi_run(lst_conf, browser)
    # sequence_run(lst_conf, browser)
    # page('config1.ini', browser)
