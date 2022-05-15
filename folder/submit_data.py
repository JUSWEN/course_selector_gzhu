import asyncio
import logging

import aiohttp


async def submit_data(student_number, data, jar):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62 ",
        "refer":
        f"http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.htmlgnmkdm=N253512&layout=default&su={student_number}"
    }

    url = f"http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzbjk_xkBcZyZzxkYzb.html?gnmkdm=N253512&su={student_number}"

    params = {"gnmkdm": "N253512", "su": student_number}

    try:
        # ClientSession别忘了跟()
        async with aiohttp.ClientSession() as session:
            async with session.post(url,
                                    headers=headers,
                                    data=data,
                                    params=params,
                                    cookies=jar,
                                    timeout=5) as response:
                contant = await response.text()

                contant1 = contant[8:15]

                if contant1 == '选课时间已过！':
                    logging.info('选课时间已过！')

                    await asyncio.sleep(5)

                    # 选课服务器暂未开放，重新运行程序发送表单
                    await submit_data(student_number, data, jar)

                elif contant1 == '出现未知异常，':
                    logging.info('服务器出现未知异常')

                    await asyncio.sleep(5)

                    # 服务器出现未知异常，重新运行程序发送表单
                    await submit_data(student_number, data, jar)

                else:
                    contant = contant[-4:]

                    if contant == '-1"}':
                        logging.info('对不起，该教学班已无余量，不可选！')

                    elif contant == '"0"}':
                        logging.info('所选教学班的上课时间与其他教学班有冲突！')

                    elif contant == '"1"}':
                        logging.info('恭喜你，选课成功！')

                    elif contant == 'tml>':
                        logging.info('cookie已失效！请等待cookie更新')

                        # 等待另一个进程更新cookie
                        await asyncio.sleep(10)

                        return 'cookie out of date'

                    else:
                        logging.info(contant)

                        await asyncio.sleep(5)
                        # 未知内容，重新运行程序发送表单

                        await submit_data(student_number, data, jar)

    except asyncio.TimeoutError:
        # 超时服务器仍未返回值，则重新运行程序发送表单
        await submit_data(student_number, data, jar)

    except Exception as e:
        logging.error(e)

        await asyncio.sleep(5)
        # 未知错误，重新运行程序发送表单

        await submit_data(student_number, data, jar)
