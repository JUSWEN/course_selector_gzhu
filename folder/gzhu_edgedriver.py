import json
import re
import sys
import time
import traceback
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

    def __init__(self,
                 student_number,
                 password,
                 logger,
                 headless='y',
                 eager='y'):
        """
        Args:
            student_number (str)\n
            password (str)\n
            headless(str)\n
            eager(str)

        If and only if headless == "y", the browser is headless\n
        If and only if eager == 'y', page load strategy is eager
        """
        self.logger = logger
        self.student_number = student_number
        self.password = password

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

        self.driver = selenium.webdriver.Edge(service=Service(
            EdgeChromiumDriverManager().install()),
                                              options=options)

        self.wdwait = WebDriverWait(self.driver, 30)

    def get_driver(self):
        return self.driver

    def login_portal(self):
        """从统一身份认证页面登陆融合门户"""
        student_number = self.student_number
        password = self.password

        self.driver.get(
            "https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fnewmy.gzhu.edu.cn%2Fup%2Fview%3Fm%3Dup"
        )

        try:
            self.wdwait.until(
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
            self.driver.execute_script(script)

        try:
            self.wdwait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//a[@title="教务系统"]/img')))
        except TimeoutException:
            pass

    def portal_loginStatus(self):
        '''
        检查融合门户登录状态，并在注销后进行登陆
        '''
        while True:
            try:
                self.driver.refresh()

                try:
                    self.wdwait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//a[@title='教务系统']/img")))
                except TimeoutException:
                    pass

                login_mark = self.driver.execute_script(
                    "return document.getElementsByClassName('h-navigation-header')[0]"
                )
                logout_mark = self.driver.execute_script(
                    "return document.getElementsByClassName('login-main-part')[0]"
                )

                if logout_mark and not login_mark:
                    self.login_portal()
                elif not logout_mark and not login_mark:
                    continue
                elif not logout_mark and login_mark:
                    break

                login_mark = self.driver.execute_script(
                    "return document.getElementsByClassName('h-navigation-header')[0]"
                )
                logout_mark = self.driver.execute_script(
                    "return document.getElementsByClassName('login-main-part')[0]"
                )

                if not logout_mark and login_mark:
                    break

            except Exception:
                self.logger.error(traceback.format_exc())

                continue

    def academicSystem_loginStatus(self):
        '''
        检查教务系统登录状态，并在注销后进行登陆
        '''
        while True:
            try:
                self.driver.refresh()

                try:
                    self.wdwait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//img[@class="media-object"]')))
                except TimeoutException:
                    pass

                logout_mark = self.driver.execute_script(
                    "return document.getElementsByClassName('img-responsive')[0]"
                )
                login_mark = self.driver.execute_script(
                    "return document.getElementsByClassName('media-object')[0]"
                )

                if logout_mark and not login_mark:
                    self.driver.close()

                    windows = self.driver.windows_handles
                    for window in windows:
                        self.driver.switch_to.window(window)

                        title = self.driver.title
                        if title == "融合门户":
                            break

                    self.portal_loginStatus()
                    self.login_academicSystem("y")
                elif not logout_mark and not login_mark:
                    continue
                elif not logout_mark and login_mark:
                    break

                logout_mark = self.driver.execute_script(
                    "return document.getElementsByClassName('img-responsive')[0]"
                )
                login_mark = self.driver.execute_script(
                    "return document.getElementsByClassName('media-object')[0]"
                )

                if not logout_mark and login_mark:
                    break

            except Exception:
                self.logger.error(traceback.format_exc())

                continue

    def login_academicSystem(self, brief="n"):
        '''
        登陆教务系统并检查融合门户登录状态\n
        If and only if brief == "n", check login status
        '''
        if brief == 'n':
            page = self.driver.page_source

            check = re.findall('融合门户', page)
            if len(check):
                self.logger.info('融合门户登录成功！')

            try:
                self.driver.find_element(By.XPATH,
                                         "//a[@title='教务系统']/img").click()
            except Exception:
                self.logger.error(traceback.format_exc())

                if not len(check):
                    self.logger.critical('融合门户登录失败！请检查学号密码是否输入正确！')
                else:
                    self.logger.critical('已成功登录融合门户，但不能找到教务系统图标按钮！')

                time.sleep(0.1)
                input("程序运行结束，回车以退出程序")
                sys.exit()

            title = self.driver.title
            if title == '融合门户':
                windows = self.driver.window_handles
                self.driver.switch_to.window(windows[-1])

            try:
                self.wdwait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//img[@class="media-object"]')))
            except TimeoutException:
                pass
        else:
            try:
                self.driver.execute_script(
                    "window.open('http://jwxt.gzhu.edu.cn/sso/driot4login')")
            except Exception:
                self.logger.error(traceback.format_exc())
            finally:
                title = self.driver.title
                if title == '融合门户':
                    windows = self.driver.window_handles
                    self.driver.switch_to.window(windows[-1])

                try:
                    self.wdwait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//img[@class="media-object"]')))
                except TimeoutException:
                    pass

    def save_cookie(self):
        '''保存Cookie到./cookies.txt'''
        # 得到dict的cookie
        dictcookies = self.driver.get_cookies()

        # json.dumps和json.loads分别是将字典转换为字符串和将字符串转换为字典的方法
        # json.loads仅支持元素用双引号括住的字典
        jsoncookies = json.dumps(dictcookies)
        with open('./cookies.txt', 'w') as file:
            # 将字符串cookie保存至txt文件中
            file.write(jsoncookies)

        self.logger.info('Cookie已更新！')

    def select_courses(self):
        '''选课并保存选课信息'''
        # j表示data表单生成成功,0为假,1为真。
        j = 0

        # i表示是第一次循环.0为假，1为真
        i = 1

        while True:
            # 第一次循环，进入选课系统，并判断是否处于选课阶段
            if i:
                for xpath in [
                        '//nav[@id="cdNav"]/ul[@class="nav navbar-nav"]/li[3]',
                        '//a[contains(text(),"自主选课")]'
                ]:
                    self.driver.find_element(By.XPATH, xpath).click()

                title = self.driver.title
                if title == '广州大学教学综合信息服务平台':
                    windows = self.driver.window_handles
                    self.driver.switch_to.window(windows[-1])

                try:
                    self.wdwait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//div[@class="navbar-header"]')))
                except TimeoutException:
                    pass

                source = self.driver.page_source
                # 通过页面信息判断是否处于选课阶段
                check = re.findall("当前不属于选课阶段", source)
                if len(check):
                    break

            self.logger.info(('=' * 11 + '*') * 5)
            self.logger.info('示例:(180111005)地理教学技能 - 1.0 学分')
            self.logger.info('课程名的左右不要留有空格！')
            self.logger.info(('=' * 11 + '*') * 5)

            time.sleep(0.1)
            # 通过课程名称进行选课操作
            course_name = input("请复制课程名并粘贴于此处:")

            # kch_id为课程名称中的数字id，如：180111005
            kch_id = course_name.split(')')[0][1:]

            try:
                self.wdwait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//button[@name='reset']"))).click()
            except TimeoutException:
                pass

            self.logger.info(('=' * 11 + '*') * 5)
            self.logger.info('主修课程请输入1，板块课体育请输入2')
            self.logger.info('通识选修请输入3，其他特殊课程请输入4')
            self.logger.info(('=' * 11 + '*') * 5)

            time.sleep(0.1)
            course_classification = int(input("请输入课程类别："))

            if course_classification == 1:
                self.driver.find_element(
                    By.XPATH,
                    '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[1]').click()

            elif course_classification == 2:
                self.driver.find_element(
                    By.XPATH,
                    '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[2]').click()

            elif course_classification == 3:
                self.driver.find_element(
                    By.XPATH,
                    '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[3]').click()

            elif course_classification == 4:
                self.driver.find_element(
                    By.XPATH,
                    '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[4]').click()

            sendkeys_button = self.driver.find_element(
                By.XPATH, '//input[@placeholder="请输入课程号或课程名称或教学班名称查询!"]')
            # ActionChains能模拟鼠标移动，点击，拖拽，长按，双击等等操作...
            ActionChains(self.driver).move_to_element(
                sendkeys_button).click().send_keys(kch_id).perform()

            self.driver.find_element(By.XPATH,
                                     '//button[@name="query"]').click()

            try:
                self.wdwait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//tr[1]/td[@class='jsxmzc']")))
            except TimeoutException:
                pass

            # 网页源代码
            page = self.driver.page_source
            # 在网页代码中找到教学班的个数
            jxb_numbers = re.findall('教学班个数.*">([1-9])</font>', page)

            if not len(jxb_numbers):
                self.logger.error('未找到教学班信息')
                self.logger.info(('=' * 11 + '*') * 5)
                self.logger.info('请检查信息是否输入正确！请检查课程类别是否正确！')
                self.logger.info('教学班名称示例:(180111005)地理教学技能 - 1.0 学分')
                self.logger.info('名称的左右两边不要留有空格！')
                self.logger.info(('=' * 11 + '*') * 5)

                continue

            i = 1

            self.logger.info("%" * 60)
            while i <= int(jxb_numbers[0]):
                # 不同的教学班的信息在不同序号的tr标签下,依次打印各个教学班的信息
                # 老师名字与职称
                teacher = self.driver.find_element(
                    By.XPATH, f"//tr[{i}]/td[@class='jsxmzc']").text
                # 上课时间
                course_time = self.driver.find_element(
                    By.XPATH, f"//tr[{i}]/td[@class='sksj']").text
                # 教学班号
                course_number = self.driver.find_element(
                    By.XPATH, f"//tr[{i}]]/td[@class='jxbmc']").text

                self.logger.info(
                    f'教学班{i},老师:{teacher},上课时间:{course_time},教学班号:{course_number}\n'
                )
                if i != int(jxb_numbers[0]):
                    self.logger.info('-' * 60)

                i += 1
            self.logger.info("%" * 60)

            self.logger.info(('=' * 11 + '*') * 5)
            self.logger.info('示例:(2021-2022-2)-131800701-1')
            self.logger.info('教学班号的左右两边不要留有空格！')
            self.logger.info(('=' * 11 + '*') * 5)

            time.sleep(0.1)
            # jxbmc为教学班号，通过输入的教学班号找到对应的jxb_ids的内容
            jxbmc = input('请复制要选择的教学班的教学班号并粘贴于此处:')

            tobeprocessed_jxb_ids = self.driver.find_element(
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
            rwlx = self.driver.execute_script(
                "document.getElementById('rwlx')['value']")
            rlkz = self.driver.execute_script(
                "document.getElementById('rlkz')['value']")
            rlzlkz = self.driver.execute_script(
                "document.getElementById('rlzlkz')['value']")
            xkxnm = self.driver.execute_script(
                "document.getElementById('xkxnm')['value']")
            xkxqm = self.driver.execute_script(
                "document.getElementById('xkxqm')['value']")
            xklc = self.driver.execute_script(
                "document.getElementById('xklc')['value']")
            kklxdm = self.driver.execute_script(
                "document.getElementById('kklxdm')['value']")
            zyh_id = self.driver.execute_script(
                "document.getElementById('zyh_id')['value']")
            njdm_id = self.driver.execute_script(
                "document.getElementById('njdm_id')['value']")
            xkkz_id = self.driver.execute_script(
                "document.getElementById('xkkz_id')['value']")

            # 下面是用xpath找属性值的函数
            cxbj = self.driver.find_element(
                By.XPATH, "//input[@name='cxbj']").get_attribute('value')
            xxkbj = self.driver.find_element(
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

            self.logger.info('选课内容添加成功！')

            time.sleep(0.1)
            check_break = input('是否继续添加选课内容[y/n]?:')
            if check_break == 'n':
                break

        self.driver.quit()

        if j:
            self.logger.info('data表单准备完成,抢课信息录入完毕。')
        else:
            self.logger.info('选课系统未开放,无法录入抢课信息，请在选课系统开放后再运行此脚本')

            time.sleep(0.1)
            input("程序运行结束，回车以退出程序")
            sys.exit()
