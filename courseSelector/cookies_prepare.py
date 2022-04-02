import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from . import wd_login


def cookies_prepare(xuhao, mima):
    while True:
        try:
            ydriver = wd_login.wd_login(xuhao, mima)

            driver = next(ydriver)

            driver.find_element(
                By.XPATH,
                '//img[@src="/up/resource/image/home/gz/app/jwxt.png"]').click(
                )

            driver = next(ydriver)

            break

        except Exception as e:
            print(e)
            print('cookies updating failed!')

            driver.quit()

    while True:
        try:
            time.sleep(10 * 60)

            windows = driver.window_handles
            for window in windows:
                driver.swith_to.window(window)

                driver.refresh()

            driver.swith_to.window(windows[-1])

            try:
                WebDriverWait(driver, 10, 0.5).until(
                    ec.visibility_of_element_located(
                        (By.XPATH, '//span[@id="xtmc"]')))
            except:
                pass

            # 得到dict的cookie
            dictcookies = driver.get_cookies()
            # json.dumps和json.loads分别是将字典转换为字符串和将字符串转换为字典的方法
            # json.loads仅支持元素用双引号括住的字典
            jsoncookies = json.dumps(dictcookies)
            with open('./cookies.txt', 'w') as file:
                # 将字符串cookie保存至txt文件中
                file.write(jsoncookies)
                file.close()

            print('cookies updated')

        # driver.refresh()可能导致异常Timed out receiving message from renderer
        # 这种异常只能重新创建webdriver
        except Exception as e:
            print(e)
            print('cookies updating failed!')

            driver.quit()

            break

    print("尝试重新登录并更新cookie")

    cookies_prepare(xuhao, mima)
