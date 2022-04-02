# 适用于gzhu新教务系统
# 谨献给745各位靓仔
# 邮箱 lihao_deng@qq.com
# 本人不对因使用此脚本而产生的任何后果或损失负责

from multiprocessing import Process, freeze_support

from courseSelector import cookies_prepare, main, qiangke

if __name__ == "__main__":
    freeze_support()

    xuhao, mima, delay = main.main()

    # 创建两个进程，一个用更新cookie以及维持会话， 一个用来发送表单抢课
    process = [
        Process(target=cookies_prepare.cookies_prepare, args=(xuhao, mima)),
        Process(target=qiangke.qiangke, args=(xuhao, delay))
    ]

    [p.start() for p in process]
    [p.join() for p in process]
