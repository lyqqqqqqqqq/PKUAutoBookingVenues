from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import quote
import time
import datetime
import warnings
import random
warnings.filterwarnings('ignore')


def login(driver, user_name, password, retry=0):
    if retry == 3:
        raise Exception('门户登录失败')

    print('门户登录中...')

    appID = 'portal2017'
    iaaaUrl = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp'
    appName = quote('北京大学校内信息门户新版')
    redirectUrl = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'

    driver.get('https://portal.pku.edu.cn/portal2017/')
    driver.get(
        f'{iaaaUrl}?appID={appID}&appName={appName}&redirectUrl={redirectUrl}')
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'logon_button')))
    driver.find_element_by_id('user_name').send_keys(user_name)
    time.sleep(0.1)
    driver.find_element_by_id('password').send_keys(password)
    time.sleep(0.1)
    driver.find_element_by_id('logon_button').click()
    try:
        WebDriverWait(driver,
                      5).until(EC.visibility_of_element_located((By.ID, 'all')))
        print('门户登录成功!')
        return '门户登录成功!\n'
    except:
        print('Retrying...')
        login(driver, user_name, password, retry + 1)
    return '门户登录失败!\n'


def go_to_venue(driver, venue, retry=0):
    if retry == 3:
        print("进入智慧场馆界面失败")
        log_str = "进入智慧场馆界面失败\n"

    print("进入预约 %s 界面" % venue)
    log_str = "进入预约 %s 界面\n" % venue
    try:
        butt_all = driver.find_element_by_id('all')
        driver.execute_script('arguments[0].click();', butt_all)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'venues')))
        driver.find_element_by_id('venues').click()
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]").click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'venueDetailBottomItem')))
        driver.find_element_by_xpath(
            '//div [contains(text(),\'%s\')]' % venue).click()
        log_str += "进入预约 %s 界面成功\n" % venue
    except:
        print("retrying")
        go_to_venue(driver, venue, retry + 1)
    return log_str


def click_agree(driver):
    print("点击同意")
    log_str = "点击同意\n"
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'ivu-checkbox-wrapper')))
    driver.find_element_by_class_name('ivu-checkbox-wrapper').click()
    print("点击同意成功\n")
    log_str += "点击同意成功\n"
    return log_str


def judge_exceeds_days_limit(start_time, end_time):
    start_time_list = start_time.split('/')
    end_time_list = end_time.split('/')
    print(start_time_list, end_time_list)
    now = datetime.datetime.today()
    today = datetime.datetime.strptime(str(now)[:10], "%Y-%m-%d")
    time_hour = datetime.datetime.strptime(
        str(now).split()[1][:-7], "%H:%M:%S")
    time_11_59 = datetime.datetime.strptime(
        "11:59:00", "%H:%M:%S")
    time_11_59 = datetime.datetime.strptime(
        "16:16:00", "%H:%M:%S")

    start_time_list_new = []
    end_time_list_new = []
    delta_day_list = []

    for k in range(len(start_time_list)):
        start_time = start_time_list[k]
        end_time = end_time_list[k]
        if len(start_time) > 8:
            date = datetime.datetime.strptime(
                start_time.split('-')[0], "%Y%m%d")
            delta_day = (date-today).days
        else:
            delta_day = (int(start_time[0])+6-today.weekday()) % 7
            date = today+datetime.timedelta(days=delta_day)
        print("日期:", str(date).split()[0])

        # print(delta_day)
        if delta_day > 3 or (delta_day == 3 and time_hour < time_11_59):
            print("只能在当天中午12:00后预约未来3天以内的场馆")
            log_str = "只能在当天中午12:00后预约未来3天以内的场馆\n"
            break
        else:
            start_time_list_new.append(start_time)
            end_time_list_new.append(end_time)
            delta_day_list.append(delta_day)
            print("在预约可预约日期范围内")
            log_str = "在预约可预约日期范围内\n"
    return start_time_list_new, end_time_list_new, delta_day_list, log_str


def book(driver, start_time_list, end_time_list, delta_day_list):
    print("查找空闲场地")
    log_str = "查找空闲场地\n"

    def judge_close_to_time_12():
        now = datetime.datetime.today()
        time_hour = datetime.datetime.strptime(
            str(now).split()[1][:-7], "%H:%M:%S")
        time_11_59 = datetime.datetime.strptime(
            "11:59:00", "%H:%M:%S")
        time_12 = datetime.datetime.strptime(
            "12:00:00", "%H:%M:%S")
        time_11_59 = datetime.datetime.strptime(
            "16:16:00", "%H:%M:%S")
        time_12 = datetime.datetime.strptime(
            "16:17:00", "%H:%M:%S")
        if time_hour < time_11_59:
            return 0
        elif time_11_59 < time_hour < time_12:
            return 1
        elif time_hour > time_12:
            return 2

    def judge_in_time_range(start_time, end_time, venue_time_range):
        vt = venue_time_range.split('-')
        vt_start_time = datetime.datetime.strptime(vt[0], "%H:%M")
        vt_end_time = datetime.datetime.strptime(vt[1], "%H:%M")
        # print(vt_start_time <= start_time)
        # print(vt_end_time >= end_time)
        if start_time <= vt_start_time and vt_end_time <= end_time:
            return True
        else:
            return False

    def click_free(start_time, end_time):
        trs = driver.find_elements_by_tag_name('tr')
        trs_list = []
        for i in range(1, len(trs)-2):
            vt = trs[i].find_elements_by_tag_name(
                'td')[0].find_element_by_tag_name('div').text
            if judge_in_time_range(start_time, end_time, vt):
                trs_list.append(trs[i].find_elements_by_tag_name(
                    'td'))
        if len(trs_list) == 0:
            return False
        # 随机点一列free的，防止每次都点第一列
        j_list = [x for x in range(1, len(trs_list[0]))]
        random.shuffle(j_list)
        print(j_list)
        for j in j_list:
            flag = False
            for i in range(len(trs_list)):
                class_name = trs_list[i][j].find_element_by_tag_name(
                    'div').get_attribute("class")
                print(class_name)
                if class_name.split()[2] == 'free':
                    flag = True
                    break
            if flag:
                for i in range(len(trs_list)):
                    trs_list[i][j].find_element_by_tag_name(
                        'div').click()
                return True
        return False

    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/form/div/div/div/div[1]/div/div/input')))

    # 若接近但是没到12点，停留在此页面
    flag = judge_close_to_time_12()
    if flag == 1:
        while True:
            flag = judge_close_to_time_12()
            if flag == 2:
                break
            else:
                time.sleep(1)
        driver.refresh()
        time.sleep(0.2)

    for k in range(len(start_time_list)):
        start_time = start_time_list[k]
        end_time = end_time_list[k]
        delta_day = delta_day_list[k]

        if k != 0:
            driver.refresh()
            time.sleep(0.2)

        for i in range(delta_day):
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/form/div/div/button[2]/i').click()
            time.sleep(0.2)

        start_time = datetime.datetime.strptime(
            start_time.split('-')[1], "%H%M")
        end_time = datetime.datetime.strptime(end_time.split('-')[1], "%H%M")
        print("开始时间:%s" % str(start_time).split()[1])
        print("结束时间:%s" % str(end_time).split()[1])

        status = click_free(start_time, end_time)
        # 如果第一页没有，就往后翻，直到不存在下一页
        while not status:
            next_table = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/thead/tr/td[6]/div/span/i')
            if len(next_table) > 0:
                driver.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/thead/tr/td[6]/div/span/i').click()
                status = click_free(start_time, end_time)
            else:
                break
        if status:
            log_str += "找到空闲场地\n"
            print("找到空闲场地\n")
            return status, log_str
        else:
            log_str += "没有空余场地\n"
            print("没有空余场地\n")
    return status, log_str


def click_book(driver):
    print("确定预约")
    log_str = "确定预约\n"
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[5]/div/div[2]')))
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[5]/div/div[2]').click()
    print("确定预约成功")
    log_str += "确定预约成功\n"
    return log_str


def click_submit_order(driver):
    print("提交订单")
    log_str = "提交订单\n"
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'payHandleItem')))
    time.sleep(0.1)
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]').click()
    #result = EC.alert_is_present()(driver)
    print("提交订单成功")
    log_str += "提交订单成功\n"
    return log_str


def click_pay(driver):
    print("付款（校园卡）")
    log_str = "付款（校园卡）\n"
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[3]/div[7]/div[2]')))
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[3]/div[2]/div/div[3]/div[7]/div[2]').click()
    print("付款成功")
    log_str += "付款成功\n"
    return log_str


def log_status(config, start_time, log_str):
    print("记录日志")
    now = datetime.datetime.now()
    with open('%s.log' % config.split('.')[0], 'a', encoding='utf-8') as fw:
        fw.write(str(now)+"\n")
        fw.write("%s\n" % str(start_time))
        fw.write(log_str+"\n")
    print("记录日志成功")


if __name__ == '__main__':
    pass
