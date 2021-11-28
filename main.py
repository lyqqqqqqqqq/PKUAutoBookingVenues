from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import warnings
import sys
import re
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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        options=chrome_options,
        executable_path=sys_path(browser="chromedriver"),
        service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    print('Driver Launched\n')

    login(driver, user_name, password, retry=0)
    go_to_venue(driver, venue)
    status = book(driver, start_time, end_time)
    if status:
        click_agree(driver)
        click_book(driver)
        click_submit_order(driver)
        click_pay(driver)
        if wechat_notice:
            wechat_notification(user_name, venue, sckey)
        status = True
    else:
        status = False
    driver.quit()
    return status


def run(config, run_times=3):
    env_check()
    for i in range(run_times):
        try:
            status = page(config)
            if status:
                break
        except:
            pass


if __name__ == '__main__':

    lst_conf = env_check()
    print(lst_conf)
    print('读取到%d份配置文件\n' % len(lst_conf))

    for num, config in enumerate(lst_conf):
        print('||第%d个预约||' % num+1)
        run(config)
