import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import gzhuWebdriver


def access_maintainCookie(student_number, password):
    while True:
        try:
            gzhuEd = gzhuWebdriver.gzhu_edgedriver(student_number, password)

            driver = gzhuEd.start_edgedriver()

            gzhuEd.login_portal(driver)

            gzhuWebdriver.login_academicSystem(driver, "y")

            gzhuWebdriver.switchto_academicSystem(driver)

            gzhuWebdriver.save_cookie(driver)

            break

        except Exception as e:
            print(e)
            print('cookies updating failed!')

            driver.quit()

    # retry为0表示不需要重试，retry为1表示需要重试
    retry = 0

    while True:
        try:
            if retry == 1:
                driver.refresh()

                retry = 0

            else:
                time.sleep(10 * 60)

            windows = driver.window_handles
            for window in windows:
                driver.switch_to.window(window)

                driver.refresh()

            driver.switch_to.window(windows[-1])

            try:
                WebDriverWait(driver, 10, 0.5).until(
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
