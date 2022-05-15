import json
import logging
import re
import sys
import urllib.parse

import selenium.webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class gzhu_edgedriver:

    def __init__(self, student_number, password):
        """
        Args:
            student_number (str)\n
            password (str)
        """
        self.student_number = student_number

        self.password = password

    def start_edgedriver(self, headless='y', eager='y'):
        """
        If and only if headless == "y", the browser is headless\n
        If and only if eager == 'y', page load strategy is eager
        """
        options = Options()

        optionsList = [
            "--enable-javascript", "start-maximized", "--disable-gpu",
            "--disable-extensions", "--no-sandbox",
            "--disable-browser-side-navigation", "--disable-dev-shm-usage"
        ]

        if headless == 'y':
            optionsList.append("--headless")

        if eager == 'y':
            options.page_load_strategy = 'eager'

        for option in optionsList:
            options.add_argument(option)

        options.add_experimental_option("excludeSwitches", [
            "ignore-certificate-errors", "enable-automation", "enable-logging"
        ])

        driver = selenium.webdriver.Edge(service=Service(
            EdgeChromiumDriverManager().install()),
                                         options=options)

        return driver

    def login_portal(self, driver):
        """从统一身份认证页面登陆融合门户"""
        wdwait = WebDriverWait(driver, 30)

        student_number = self.student_number
        password = self.password

        driver.get(
            "https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fnewmy.gzhu.edu.cn%2Fup%2Fview%3Fm%3Dup"
        )

        try:
            wdwait.until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     "//div[@class='robot-mag-win small-big-small']")))

        except TimeoutException:
            pass

        for script in [
                f"document.getElementById('un').value='{student_number}'",
                f"document.getElementById('pd').value='{password}'",
                "document.getElementById('index_login_btn').click()"
        ]:
            driver.execute_script(script)

        try:
            wdwait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//a[@title="教务系统"]/img')))

        except TimeoutException:
            pass

    def portal_loginStatus(self, driver):
        '''
        检查融合门户登录状态，并在注销后进行登陆
        '''
        wdwait = WebDriverWait(driver, 30)

        while True:
            try:
                driver.refresh()

                try:
                    wdwait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//a[@title='教务系统']/img")))

                except TimeoutException:
                    pass

                login_mark = driver.execute_script(
                    "return document.getElementsByClassName('h-navigation-header')[0]"
                )

                if login_mark == None:
                    self.login_portal(driver)
                else:
                    break

                login_mark = driver.execute_script(
                    "return document.getElementsByClassName('h-navigation-header')[0]"
                )

                if login_mark != None:
                    break

            except Exception as e:
                logging.error(e)

                continue

    def academicSystem_loginStatus(self, driver):
        '''
        检查教务系统登录状态，并在注销后进行登陆
        '''
        wdwait = WebDriverWait(driver, 30)

        while True:
            try:
                driver.refresh()

                try:
                    wdwait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//img[@class="media-object"]')))

                except TimeoutException:
                    pass

                logout_mark = driver.execute_script(
                    "return document.getElementsByClassName('img-responsive')[0]"
                )

                if logout_mark != None:
                    driver.close()

                    windows = driver.windows_handles
                    for window in windows:
                        driver.switch_to.window(window)

                        title = driver.title
                        if title == "融合门户":
                            break

                    self.portal_loginStatus(driver)

                    login_academicSystem(driver, "y")

                else:
                    break

                logout_mark = driver.execute_script(
                    "return document.getElementsByClassName('img-responsive')[0]"
                )

                if logout_mark == None:
                    break

            except Exception as e:
                logging.error(e)

                continue


def login_academicSystem(driver, brief="n"):
    '''
    登陆教务系统并检查融合门户登录状态\n
    If and only if brief == "n", check login status
    '''
    wdwait = WebDriverWait(driver, 30)

    if brief == 'n':
        page = driver.page_source
        check = re.findall('融合门户', page)
        if len(check) != 0:
            logging.info('融合门户登录成功！')

        try:
            driver.find_element(By.XPATH, "//a[@title='教务系统']/img").click()

        except Exception as e:
            logging.error(e)

            if len(check) == 0:
                logging.critical('融合门户登录失败！\n'
                                 '请检查学号密码是否输入正确！\n'
                                 '并重新运行程序！')

            else:
                logging.critical('未知错误\n'
                                 '已成功登录融合门户，但不能找到教务系统图标按钮！\n'
                                 '请重新运行程序！')

            input("程序运行结束，回车以退出程序")

            sys.exit(0)

        title = driver.title
        if title == '融合门户':
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])

    else:
        driver.execute_script(
            "window.open('http://jwxt.gzhu.edu.cn/sso/driot4login')")

    try:
        wdwait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//img[@class="media-object"]')))

    except TimeoutException:
        pass


def save_cookie(driver):
    '''保存Cookie到./cookies.txt'''
    # 得到dict的cookie
    dictcookies = driver.get_cookies()
    # json.dumps和json.loads分别是将字典转换为字符串和将字符串转换为字典的方法
    # json.loads仅支持元素用双引号括住的字典
    jsoncookies = json.dumps(dictcookies)
    with open('./cookies.txt', 'w') as file:
        # 将字符串cookie保存至txt文件中
        file.write(jsoncookies)

    logging.info('cookies updated')


def select_courses(driver):
    '''自主选课'''
    wdwait = WebDriverWait(driver, 30)

    # j表示data表单生成成功,0为假,1为真。
    j = 0

    # i表示是第一次循环.0为假，1为真
    i = 1

    while True:
        # 第一次循环，进入选课系统，并判断是否处于选课阶段
        if i == 1:
            for xpath in [
                    '//nav[@id="cdNav"]/ul[@class="nav navbar-nav"]/li[3]',
                    '//a[contains(text(),"自主选课")]'
            ]:
                driver.find_element(By.XPATH, xpath).click()

            title = driver.title
            if title == '广州大学教学综合信息服务平台':
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])

            try:
                wdwait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//div[@class="navbar-header"]')))

            except TimeoutException:
                pass

            source = driver.page_source
            # 通过页面信息判断是否处于选课阶段
            check = re.findall("当前不属于选课阶段", source)
            if len(check) != 0:
                break

        # 通过课程名称进行选课操作
        course_name = input('请完整复制课程名并粘贴于此处,示例:(180111005)地理教学技能 - 1.0 学分\n'
                            '注意！课程名的左右不要留有空格！\n')

        # kch_id为课程名称中的数字id，如：180111005
        kch_id = course_name.split(')')[0][1:]

        try:
            wdwait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//button[@name='reset']"))).click()

        except TimeoutException:
            pass

        course_classification = int(
            input('请输入课程类别：\n主修课程请输入1，板块课体育请输入2，通识选修请输入3，其他特殊课程请输入4\n'))

        if course_classification == 1:
            driver.find_element(
                By.XPATH,
                '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[1]').click()

        elif course_classification == 2:
            driver.find_element(
                By.XPATH,
                '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[2]').click()

        elif course_classification == 3:
            driver.find_element(
                By.XPATH,
                '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[3]').click()

        elif course_classification == 4:
            driver.find_element(
                By.XPATH,
                '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[4]').click()

        sendkeys_button = driver.find_element(
            By.XPATH, '//input[@placeholder="请输入课程号或课程名称或教学班名称查询!"]')
        # ActionChains能模拟鼠标移动，点击，拖拽，长按，双击等等操作...
        ActionChains(driver).move_to_element(
            sendkeys_button).click().send_keys(kch_id).perform()

        driver.find_element(By.XPATH, '//button[@name="query"]').click()

        try:
            wdwait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//tr[1]/td[@class='jsxmzc']")))

        except TimeoutException:
            pass

        # 网页源代码
        page = driver.page_source
        # 在网页代码中找到教学班的个数
        jxb_numbers = re.findall('教学班个数.*">([1-9])</font>', page)

        if len(jxb_numbers) == 0:
            logging.error('未找到教学班信息，请检查信息是否输入正确\n'
                          '教学班名称示例:(180111005)地理教学技能 - 1.0 学分\n'
                          '注意！名称的左右不要留有空格！\n'
                          '注意！请检查课程类别是否正确！\n'
                          '请在程序提示后，重新输入信息！')

            continue

        i = 1

        while i <= int(jxb_numbers[0]):
            # 不同的教学班的信息在不同序号的tr标签下,依次打印各个教学班的信息
            # 老师名字与职称
            teacher = driver.find_element(
                By.XPATH, f"//tr[{i}]/td[@class='jsxmzc']").text
            # 上课时间
            course_time = driver.find_element(
                By.XPATH, f"//tr[{i}]/td[@class='sksj']").text
            # 教学班号
            course_number = driver.find_element(
                By.XPATH, f"//tr[{i}]]/td[@class='jxbmc']").text

            logging.info(
                f'教学班{i},老师:{teacher},上课时间:{course_time},教学班号:{course_number}\n'
            )

            i += 1

        # jxbmc为教学班号，通过输入的教学班号找到对应的jxb_ids的内容
        jxbmc = input('请从上面的教学班中选择并复制粘贴要选择的教学班的教学班号\n'
                      '示例:(2021-2022-2)-131800701-1\n'
                      '注意！教学班号的左右不要留有空格！\n')

        tobeprocessed_jxb_ids = driver.find_element(
            By.XPATH,
            f'//td[@class="jxbmc" and contains(text(), "{jxbmc}")]/../td[@class="an"]/button'
        ).get_attribute('onclick')

        jxb_ids = tobeprocessed_jxb_ids.split(',')[1][1:-1]

        # 下面是求kcmc的函数
        course_name = course_name.split(')')
        course_name[0] = course_name[0] + ')'

        strings = course_name[1].split(' ')
        strings1 = urllib.parse.quote(strings[0])
        strings2 = urllib.parse.quote(strings[-1])

        # kcmc通过urlencode编码，但是，kcmc只有部分编码，需要注意
        kcmc = course_name[0] + strings1 + '+-+1.0+' + strings2

        # 下面为通过js找到属性值的函数
        rwlx = driver.execute_script(
            "document.getElementById('rwlx')['value']")
        rlkz = driver.execute_script(
            "document.getElementById('rlkz')['value']")
        rlzlkz = driver.execute_script(
            "document.getElementById('rlzlkz')['value']")
        xkxnm = driver.execute_script(
            "document.getElementById('xkxnm')['value']")
        xkxqm = driver.execute_script(
            "document.getElementById('xkxqm')['value']")
        xklc = driver.execute_script(
            "document.getElementById('xklc')['value']")
        kklxdm = driver.execute_script(
            "document.getElementById('kklxdm')['value']")
        zyh_id = driver.execute_script(
            "document.getElementById('zyh_id')['value']")
        njdm_id = driver.execute_script(
            "document.getElementById('njdm_id')['value']")
        xkkz_id = driver.execute_script(
            "document.getElementById('xkkz_id')['value']")

        # 下面是用xpath找属性值的函数
        cxbj = driver.find_element(
            By.XPATH, "//input[@name='cxbj']").get_attribute('value')
        xxkbj = driver.find_element(
            By.XPATH, "//input[@name='xxkbj']").get_attribute('value')

        # 下面是完整的data表单的内容
        # sxbj与qz的属性没有在页面中找到,通过抓包获得
        data = {
            "jxb_ids": jxb_ids,
            "kch_id": kch_id,
            "kcmc": kcmc,
            "rwlx": rwlx,
            "rlkz": rlkz,
            "rlzlkz": rlzlkz,
            "sxbj": "1",
            "xxkbj": xxkbj,
            "qz": "0",
            "cxbj": cxbj,
            "xkkz_id": xkkz_id,
            "njdm_id": njdm_id,
            "zyh_id": zyh_id,
            "kklxdm": kklxdm,
            "xklc": xklc,
            "xkxnm": xkxnm,
            "xkxqm": xkxqm
        }

        with open('./data.txt', 'a') as data_file:
            # dict类型的内容不能用write函数
            data_file.write(str(data) + '\n')

        # j=1 表示抢课信息录入成功
        j = 1

        # i=0表示不是第一循环
        i = 0

        logging.info('选课内容添加成功！')

        check_break = input('是否继续添加选课内容[y/n]?:')
        if check_break == 'n':
            break

    driver.quit()

    if j:
        logging.info('data表单准备完成,抢课信息录入完毕。')
    else:
        logging.info('选课系统未开放,无法录入抢课信息，请在选课系统开放后再运行此脚本')

        input("程序运行结束，回车以退出程序")

        sys.exit()
