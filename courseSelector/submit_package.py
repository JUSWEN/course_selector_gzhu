import asyncio

import aiohttp


async def submit_package(xuhao, data, jar):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62 ",
        "refer":
        f"http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.htmlgnmkdm=N253512&layout=default&su={xuhao}"
    }

    url = f"http://jwxt.gzhu.edu.cn/jwglxt/xsxk/zzxkyzbjk_xkBcZyZzxkYzb.html?gnmkdm=N253512&su={xuhao}"

    params = {"gnmkdm": "N253512", "su": xuhao}

    try:
        # ClientSession别忘了跟()
        async with aiohttp.ClientSession() as session:
            async with await session.post(url,
                                          headers=headers,
                                          data=data,
                                          params=params,
                                          cookies=jar,
                                          timeout=5) as response:
                contant = await response.text()

                contant1 = contant[8:15]

                if contant1 == '选课时间已过！':
                    print('选课时间已过！')

                    await asyncio.sleep(5)

                    # 选课服务器暂未开放，重新运行程序发送表单
                    await submit_package(xuhao, data, jar)

                elif contant1 == '出现未知异常，':
                    print('服务器出现未知异常')

                    await asyncio.sleep(5)

                    # 服务器出现未知异常，重新运行程序发送表单
                    await submit_package(xuhao, data, jar)

                else:
                    contant = contant[-4:]

                    if contant == '-1"}':
                        print('对不起，该教学班已无余量，不可选！')

                    elif contant == '"0"}':
                        print('所选教学班的上课时间与其他教学班有冲突！')

                    elif contant == '"1"}':
                        print('恭喜你，选课成功！')

                    elif contant == 'tml>':
                        print('cookie已失效！请等待cookie更新')

                        # 等待另一个进程更新cookie
                        await asyncio.sleep(10)

                        return 'cookie out of date'

                    else:
                        print(contant)

                        await asyncio.sleep(5)
                        # 未知内容，重新运行程序发送表单

                        await submit_package(xuhao, data, jar)

    except asyncio.TimeoutError:
        # 超时服务器仍未返回值，则重新运行程序发送表单
        await submit_package(xuhao, data, jar)

    except Exception as e:
        print(e)

        await asyncio.sleep(5)
        # 未知错误，重新运行程序发送表单

        await submit_package(xuhao, data, jar)
