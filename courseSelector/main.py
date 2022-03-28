import imp
import os
import re
import sys
import urllib.parse
from multiprocessing import Process

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from . import cookies_prepare
from . import qiangke
from . import wd_login
from . import xuehao_mima


def main(driver_path):
    xuhao, mima = xuehao_mima.xuehao_mima()

    data_txt = os.path.exists('./data.txt')

    # 如果没有data.txt选课信息表单，就要求用户输入选课信息，生成表单
    if not data_txt:
        ydriver = wd_login.wd_login(driver_path, xuhao, mima)

        driver = next(ydriver)

        page = driver.page_source
        judge = re.findall('融合门户', page)
        if len(judge) != 0:
            print('融合门户登录成功！')

        try:
            driver.find_element_by_xpath(
                '//img[@src="/up/resource/image/home/gz/app/jwxt.png"]').click(
                )
        except Exception as e:
            print(e)

            if len(judge) == 0:
                print('融合门户登录失败！')
                print('请检查学号密码是否输入正确！\n程序结束')

            else:
                print('unknown error!')
                print('已成功登录融合门户，但不能找到教务系统图标按钮！')
                print('重新运行程序或重启电脑或许能解决问题！')

            sys.exit(0)

        xuehao_mima.save_xuhaoMima(xuhao, mima)

        driver = next(ydriver)

        # j表示data表单生成成功,0为假,1为真。
        j = 0

        # i表示是第一次循环.0为假，1为真
        i = 1

        while True:
            # 第一次循环，判断是否处于选课阶段
            if i == 1:
                source = driver.page_source
                # 通过页面信息判断是否处于选课阶段
                judge = re.findall("当前不属于选课阶段", source)
                if len(judge) != 0:
                    break

            # 通过课程名称进行选课操作
            course_name = input(
                '请完整复制课程名并粘贴于此处,示例:(180111005)地理教学技能 - 1.0 学分\n注意！课程名的左右不要留有空格！\n'
            )

            # kch_id为课程名称中的数字id，如：180111005
            kch_id = course_name.split(')')[0][1:]

            try:
                WebDriverWait(driver, 10, 0.5).until(
                    ec.visibility_of_element_located(
                        (By.XPATH, "//button[@name='reset']")))
            except:
                pass

            # execute_script可以在selenium中执行js命令
            driver.execute_script(
                'document.getElementsByName("reset")[0].click();')

            course_classification = int(
                input('请输入课程类别：\n主修课程请输入1，板块课体育请输入2，通识选修请输入3，其他特殊课程请输入4\n'))

            if course_classification == 1:
                driver.find_element_by_xpath(
                    '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[1]').click()

            elif course_classification == 2:
                driver.find_element_by_xpath(
                    '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[2]').click()

            elif course_classification == 3:
                driver.find_element_by_xpath(
                    '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[3]').click()

            elif course_classification == 4:
                driver.find_element_by_xpath(
                    '//ul[@class="nav nav-tabs sl_nav_tabs"]/li[4]').click()

            sendkeys_button = driver.find_element_by_xpath(
                '//input[@placeholder="请输入课程号或课程名称或教学班名称查询!"]')
            # ActionChains能模拟鼠标移动，点击，拖拽，长按，双击等等操作...
            ActionChains(driver).move_to_element(
                sendkeys_button).click().send_keys(kch_id).perform()

            driver.find_element_by_xpath('//button[@name="query"]').click()

            try:
                WebDriverWait(driver, 10, 0.5).until(
                    ec.visibility_of_element_located(
                        (By.XPATH, "//tr[1]/td[@class='jsxmzc']")))
            except:
                pass

            # 网页源代码
            page = driver.page_source
            # 在网页代码中找到教学班的个数
            jxb_numbers = re.findall('教学班个数.*">([1-9])</font>', page)

            if len(jxb_numbers) == 0:
                print('未找到教学班信息，请检查信息是否输入正确')
                print(
                    '教学班名称示例:(180111005)地理教学技能 - 1.0 学分\n注意！名称的左右不要留有空格！\n注意！请检查课程类别是否正确！'
                )
                print('请在程序提示后，重新输入信息！')

                continue

            i = 1

            while i <= int(jxb_numbers[0]):
                # 不同的教学班的信息在不同序号的tr标签下,依次打印各个教学班的信息
                # 老师名字与职称
                teacher = driver.find_element_by_xpath(
                    "//tr[%d]/td[@class='jsxmzc']" % i).text
                # 上课时间
                course_time = driver.find_element_by_xpath(
                    "//tr[%d]/td[@class='sksj']" % i).text
                # 教学班号
                course_number = driver.find_element_by_xpath(
                    "//tr[%d]/td[@class='jxbmc']" % i).text

                print('教学班%d,老师:%s,上课时间:%s,教学班号:%s\n' %
                      (i, teacher, course_time, course_number))

                i += 1

            # jxbmc为教学班号，通过输入的教学班号找到对应的jxb_ids的内容
            jxbmc = input(
                '请从上面的教学班中选择并复制粘贴要选择的教学班的教学班号，示例:(2021-2022-2)-131800701-1\n注意！教学班号的左右不要留有空格！\n'
            )
            tobeprocessed_jxb_ids = driver.find_element_by_xpath(
                '//td[@class="jxbmc" and contains(text(), "%s")]/../td[@class="an"]/button'
                % jxbmc).get_attribute('onclick')
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
            cxbj = driver.find_element_by_xpath(
                "//input[@name='cxbj']").get_attribute('value')
            xxkbj = driver.find_element_by_xpath(
                "//input[@name='xxkbj']").get_attribute('value')

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

            # 存储data表单
            with open('./data.txt', 'a') as data_file:
                # dict类型的内容不能用write函数
                data_file.write(str(data) + '\n')
                data_file.close()

            # j=1 表示抢课信息录入成功
            j = 1

            # i=0表示不是第一循环
            i = 0

            print('选课内容添加成功！')

            judge_break = input('是否继续添加选课内容[y/n]?:')
            if judge_break == 'n':
                break

        driver.quit()

        if j == 1:
            print('data表单准备完成,抢课信息录入完毕。')
        elif j == 0:
            print('选课系统未开放,无法录入抢课信息，请在选课系统开放后再运行此脚本')

            sys.exit()

    # 如果有抢课信息表单，则继续运行程序
    else:
        print('已存在抢课信息，如需重新选择抢课信息，请停止运行程序\n并删除此脚本当前目录下的"data.txt"文件,然后重新运行程序')

    # 创建两个进程，一个用来每二十分钟更新一次cookie， 一个用来发送表单抢课
    process = [
        Process(target=cookies_prepare.cookies_prepare,
                args=(driver_path, xuhao, mima)),
        Process(target=qiangke.qiangke, args=(xuhao, ))
    ]

    [p.start() for p in process]
    [p.join() for p in process]
