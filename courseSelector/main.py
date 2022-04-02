import os
import re
import sys

from selenium.webdriver.common.by import By

from . import xuehao_mima, wd_login


def main():
    xuhao, mima = xuehao_mima.xuehao_mima()

    data_txt = os.path.exists('./data.txt')

    # 如果没有data.txt选课信息表单，就要求用户输入选课信息，生成表单
    if not data_txt:
        ydriver = wd_login.wd_login(xuhao, mima)

        driver = next(ydriver)

        page = driver.page_source
        judge = re.findall('融合门户', page)
        if len(judge) != 0:
            print('融合门户登录成功！')

        try:
            driver.find_element(
                By.XPATH,
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

            input()

            sys.exit(0)

        xuehao_mima.save_xuhaoMima(xuhao, mima)

        next(ydriver)

        pString = next(ydriver)
        print(pString)
        if pString == '选课系统未开放,无法录入抢课信息，请在选课系统开放后再运行此脚本':
            input()

            sys.exit()

    # 如果有抢课信息表单，则继续运行程序
    else:
        print('已存在抢课信息，如需重新选择抢课信息，请停止运行程序\n'
              '并删除此脚本当前目录下的"data.txt"文件,然后重新运行程序')

    delay = input("请输入延时执行抢课的分钟数，建议延时至抢课前3到4分钟\n"
                  "如果直接Enter，则延时为0。抢课进程将在延时的分钟数后开始执行，\n"
                  "另一个进程将立即执行，登陆教务系统，维持会话并定时更新cookie\n"
                  "请输入延时分钟数：")

    if delay == '':
        delay = 0
    else:
        delay = int(delay) * 60

    return (xuhao, mima, delay)
