import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from . import gzhuWebdriver


def access_maintainCookie(student_number, password):
    # pageName用来表示当前页面标题
    # 0表示初始页面，Unified Identity Authentication页面, 统一身份认证页面和其它页面
    pageName = 0

    while True:
        gzhuEd = gzhuWebdriver.gzhu_edgedriver(student_number, password)

        driver = gzhuEd.start_edgedriver()

        try:
            driver.refresh()

            title = driver.title
            if title == '融合门户':
                pageName = 1
            elif title == '广州大学教学综合信息服务平台':
                pageName = 2
            else:
                pageName = 0

            if pageName == 0:
                gzhuEd.login_portal(driver)

            if pageName in [0, 1]:
                gzhuWebdriver.login_academicSystem(driver, 'y')

            if pageName in [0, 1, 2]:
                gzhuWebdriver.save_cookie(driver)

            break

        except Exception as e:
            print(e)
            print("cookie updating failed！")

            continue

    # retry为0表示不需要重试，retry为1表示需要重试
    retry = 0

    while True:
        try:
            if retry == 1:
                time.sleep(5)

                retry = 0

            else:
                time.sleep(10 * 60)

            windows = driver.window_handles
            for window in windows:
                driver.switch_to.window(window)

                driver.refresh()

            driver.switch_to.window(windows[-1])

            try:
                WebDriverWait(driver, 30).until(
                    ec.visibility_of_element_located(
                        (By.XPATH, '//span[@id="xtmc"]')))
            except:
                pass

            gzhuWebdriver.save_cookie(driver)

        except Exception as e:
            print(e)
            print('cookies updating failed!')

            retry = 1

            continue
