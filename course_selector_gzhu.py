# 适用于广大新版教务系统

import time
from multiprocessing import Process, freeze_support

from loguru import logger

from folder import (access_maintainCookie, check_creatData, logger_configure,
                    qiangke, studentNumber_password)

if __name__ == "__main__":
    freeze_support()

    logger_configure.configure_logger()

    logger.info("#" * 26 + "开始运行" + "#" * 26)
    time.sleep(0.1)

    if input("是否开启无头浏览器模式[y/n](正常使用需要开启，直接回车则默认开启）") == 'n':
        headless = 'n'
    else:
        headless = 'y'

    check_creatData.check_creatData(headless)

    student_number, password = studentNumber_password.access()

    logger.info(('=' * 11 + '*') * 5)
    logger.info("建议延时至选课开始前3到4分钟时开始执行抢课进程")
    logger.info("用来抢课的进程将在延时的分钟数后开始执行")
    logger.info("更新Cookie并维持登录状态的进程将立即执行")
    logger.info(('=' * 11 + '*') * 5)

    time.sleep(0.1)
    delay = input("请输入延时分钟数(如果直接Enter则立即执行):")

    if not delay:
        delay = 0
    else:
        delay = int(delay) * 60

    # 创建两个进程，一个用更新cookie以及维持会话， 一个用来发送表单抢课
    process = [
        Process(target=access_maintainCookie.access_maintainCookie,
                args=(student_number, password, headless)),
        Process(target=qiangke.qiangke, args=(student_number, delay))
    ]

    [p.start() for p in process]
    [p.join() for p in process]
