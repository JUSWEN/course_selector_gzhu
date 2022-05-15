import logging
import os

from . import gzhuWebdriver, studentNumber_password


def check_creatData():
    data_txt = os.path.exists('./data.txt')

    # 如果没有data.txt选课信息表单，就要求用户输入选课信息，生成表单
    if not data_txt:
        student_number, password = studentNumber_password.access()

        gzhuEd = gzhuWebdriver.gzhu_edgedriver(student_number, password)

        driver = gzhuEd.start_edgedriver(headless='n',eager='n')

        gzhuEd.login_portal(driver)

        gzhuWebdriver.login_academicSystem(driver)

        studentNumber_password.save(student_number, password)

        gzhuWebdriver.save_cookie(driver)

        gzhuWebdriver.select_courses(driver)

    # 如果有抢课信息表单，则继续运行程序
    else:
        logging.info('已存在抢课信息，如需重新选择抢课信息，请停止运行程序\n'
                     '并删除此脚本当前目录下的"data.txt"文件,然后重新运行程序')
