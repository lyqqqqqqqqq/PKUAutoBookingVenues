from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import quote
import time
import datetime
import warnings
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
        print('门户登录成功！')
    except:
        print('Retrying...')
        login(driver, user_name, password, retry + 1)


def go_to_venue(driver, venue):
    print("进入预约 %s 界面" % venue)
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


def click_agree(driver):
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'ivu-checkbox-wrapper')))
    driver.find_element_by_class_name('ivu-checkbox-wrapper').click()

    # <label data-v-97852f88="" class="text-left ivu-checkbox-wrapper ivu-checkbox-wrapper-checked ivu-checkbox-default"><span class="ivu-checkbox ivu-checkbox-checked"><span class="ivu-checkbox-inner"></span> <input type="checkbox" class="ivu-checkbox-input"></span>  已阅读并同意 </label>


def book(driver, start_time, end_time):
    print("查找空闲场地")

    def judge_in_time_range(venue_time_range):
        vt = venue_time_range.split('-')
        vt_start_time = datetime.datetime.strptime(vt[0], "%H:%M")
        vt_end_time = datetime.datetime.strptime(vt[1], "%H:%M")
        # print(vt_start_time <= start_time)
        # print(vt_end_time >= end_time)
        if start_time <= vt_start_time and vt_end_time <= end_time:
            return True
        else:
            return False

    def click_free():
        trs = driver.find_elements_by_tag_name('tr')
        trs_list = []
        for i in range(1, len(trs)-2):
            vt = trs[i].find_elements_by_tag_name(
                'td')[0].find_element_by_tag_name('div').text
            if judge_in_time_range(vt):
                trs_list.append(trs[i].find_elements_by_tag_name(
                    'td'))
        if len(trs_list) == 0:
            return False
        for j in range(1, len(trs_list[0])):
            flag = True
            for i in range(len(trs_list)):
                class_name = trs_list[i][j].find_element_by_tag_name(
                    'div').get_attribute("class")
                if class_name.split()[2] == 'reserved':
                    flag = False
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

    start_time_list = start_time.split('/')
    end_time_list = end_time.split('/')
    print(start_time_list, end_time_list)
    now = datetime.datetime.today()
    today = datetime.datetime.strptime(str(now)[:10], "%Y-%m-%d")

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
        print("日期：", str(date).split()[0])

        # print(delta_day)
        if delta_day > 3:
            print("只能预约3天以内的场馆")
        for i in range(delta_day):
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/form/div/div/button[2]/i').click()
            time.sleep(2)

        start_time = datetime.datetime.strptime(
            start_time.split('-')[1], "%H%M")
        end_time = datetime.datetime.strptime(end_time.split('-')[1], "%H%M")
        print("开始时间：%s" % str(start_time).split()[1])
        print("结束时间：%s" % str(end_time).split()[1])

        status = click_free()
        while not status:
            next_table = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/thead/tr/td[6]/div/span/i')
            if len(next_table) > 0:
                driver.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/thead/tr/td[6]/div/span/i').click()
                status = click_free()
            else:
                break
        if status:
            print("找到空闲场地")
            return status
        else:
            print("没有空余场地")
    return status


def click_book(driver):
    print("确定预约")
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[5]/div/div[2]')))
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[5]/div/div[2]').click()


def click_submit_order(driver):
    print("提交预约申请")
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]')))
    time.sleep(3)
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]').click()


def click_pay(driver):
    print("付款（校园卡）")
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[3]/div[7]/div[2]')))
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[3]/div[2]/div/div[3]/div[7]/div[2]').click()


if __name__ == '__main__':
    pass
