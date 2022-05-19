import asyncio
import json
import os
import sys
import time
import traceback

from loguru import logger
from requests.cookies import RequestsCookieJar

from . import submit_data


def qiangke(student_number, delay):
    try:
        time.sleep(delay)

        logger.info('开始抢课！')

        cookie_txt = os.path.exists('./cookies.txt')

        # 如果不存在cookie文件
        if not cookie_txt:
            while True:
                time.sleep(10)

                cookie_txt = os.path.exists('./cookies.txt')
                if cookie_txt:
                    break

        with open('./cookies.txt', 'r') as file:
            listcookies = json.loads(file.read())

        jar = RequestsCookieJar()
        jar.set(listcookies[0]['name'], listcookies[0]['value'])

        # 读取保存的data表单,并通过async异步的方式发送
        with open('./data.txt', 'r') as data_file:
            tobeprocessed_data = data_file.read()

        datas = tobeprocessed_data.split('\n')

        while True:
            tasks = []

            n = 0

            while n < 10:
                i = 0

                while i < len(datas) - 1:
                    data = eval(datas[i])

                    coroutine = submit_data.submit_data(
                        student_number, data, jar)
                    task = asyncio.ensure_future(coroutine)
                    tasks.append(task)

                    i += 1

                n += 1

            loop = asyncio.get_event_loop()
            result_list = loop.run_until_complete(asyncio.wait(tasks))

            # i表示cookie失效，需要重新发包
            i = 0

            for results in result_list:
                for result in results:
                    if result.result() == 'Cookie已失效':
                        i = 1

                        break

                if i:
                    break

            if i:
                with open('./cookies.txt', 'r') as file:
                    listcookies = json.loads(file.read())

                jar = RequestsCookieJar()
                jar.set(listcookies[0]['name'], listcookies[0]['value'])
            else:
                break

        loop.close()

        logger.info('抢课结束！此进程结束')
        sys.exit()
    except Exception:
        logger.error(traceback.format_exc())
        logger.info("运行错误，此进程结束")
        sys.exit()
