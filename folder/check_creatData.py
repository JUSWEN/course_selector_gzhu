import os

from loguru import logger

from . import studentNumber_password
from .gzhu_edgedriver import gzhu_edgedriver


def check_creatData(headless):
    data_txt = os.path.exists('./data.txt')

    # 如果没有data.txt选课信息表单，就要求用户输入选课信息，生成表单
    if not data_txt:
        student_number, password = studentNumber_password.access()
        gzhuEd = gzhu_edgedriver(student_number,
                                 password,
                                 headless=headless,
                                 eager='n')

        gzhuEd.login_portal()
        gzhuEd.login_academicSystem()

        studentNumber_password.save(student_number, password)
        gzhuEd.save_cookie()

        gzhuEd.select_courses()
    # 如果有抢课信息表单，则继续运行程序
    else:
        logger.info('已存在抢课信息，如需重新选择抢课信息，请停止运行程序')
        logger.info('然后删除此程序同级目录下的"data.txt"文件,最后重新运行程序')
