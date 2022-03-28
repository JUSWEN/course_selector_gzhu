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

        pString = next(ydriver)
        print(pString)
        if pString == '选课系统未开放,无法录入抢课信息，请在选课系统开放后再运行此脚本':
            sys.exit()

    # 如果有抢课信息表单，则继续运行程序
    else:
        print('已存在抢课信息，如需重新选择抢课信息，请停止运行程序\n'
              '并删除此脚本当前目录下的"data.txt"文件,然后重新运行程序')

    # 创建两个进程，一个用来每二十分钟更新一次cookie， 一个用来发送表单抢课
    process = [
        Process(target=cookies_prepare.cookies_prepare,
                args=(driver_path, xuhao, mima)),
        Process(target=qiangke.qiangke, args=(xuhao, ))
    ]

    [p.start() for p in process]
    [p.join() for p in process]
