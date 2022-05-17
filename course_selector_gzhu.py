# 适用于广大新版教务系统

import logging
from multiprocessing import Process, freeze_support

from folder import (access_maintainCookie, check_creatData, qiangke,
                    studentNumber_password)

if __name__ == "__main__":
    freeze_support()

    if input("是否开启debug模式[y/n](直接回车则不开启）") == 'y':
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(processName)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(
            level=logging.INFO,
            format='%(processName)s - %(levelname)s - %(message)s')

    check_creatData.check_creatData()

    student_number, password = studentNumber_password.access()

    delay = input("请输入延时执行抢课的分钟数，建议延时至抢课前3到4分钟\n"
                  "如果直接Enter，则延时为0。抢课进程将在延时的分钟数后开始执行，\n"
                  "另一个进程将立即执行，登陆教务系统，维持会话并定时更新cookie\n"
                  "请输入延时分钟数：")

    if delay == '':
        delay = 0
    else:
        delay = int(delay) * 60

    # 创建两个进程，一个用更新cookie以及维持会话， 一个用来发送表单抢课
    process = [
        Process(target=access_maintainCookie.access_maintainCookie,
                args=(student_number, password)),
        Process(target=qiangke.qiangke, args=(student_number, delay))
    ]

    [p.start() for p in process]
    [p.join() for p in process]