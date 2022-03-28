import time

from . import wd_login


def cookies_prepare(driver_path, xuhao, mima):
    while True:
        try:
            ydriver = wd_login.wd_login(driver_path, xuhao, mima)

            driver = next(ydriver)

            driver.find_element_by_xpath(
                '//img[@src="/up/resource/image/home/gz/app/jwxt.png"]').click(
                )

            driver = next(ydriver)

            # 等待1100秒,差不多20分钟更新一次cookie
            time.sleep(1100)

            driver.quit()

        except Exception as e:
            print(e)
            print('cookies updating failed!')

            driver.quit()
