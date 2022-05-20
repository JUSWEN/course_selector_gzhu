import time
import traceback

from .gzhu_edgedriver import gzhu_edgedriver


def access_maintainCookie(student_number, password, headless, logger):
    # pageName用来表示当前页面标题
    # 0表示初始页面，Unified Identity Authentication页面, 统一身份认证页面和其它页面
    pageName = 0
    gzhuEd = gzhu_edgedriver(student_number, password, logger, headless)

    driver = gzhuEd.get_driver()

    while True:
        try:
            driver.refresh()

            title = driver.title
            if title == '融合门户':
                pageName = 1
            elif title == '广州大学教学综合信息服务平台':
                pageName = 2
            elif title == '':
                continue
            else:
                pageName = 0

            if not pageName:
                gzhuEd.login_portal()
                continue
            if pageName in [0, 1]:
                gzhuEd.login_academicSystem('y')
            if pageName in [0, 1, 2]:
                gzhuEd.academicSystem_loginStatus()
                gzhuEd.save_cookie()

            break
        except Exception:
            logger.error("Cookie更新失败！")
            logger.error(traceback.format_exc())

    # retry为0表示不需要重试，retry为1表示需要重试
    retry = 0

    while True:
        try:
            if retry:
                retry = 0
            else:
                time.sleep(5 * 60)

            windows = driver.window_handles
            for window in windows:
                driver.switch_to.window(window)

                title = driver.title
                if title == '融合门户':
                    gzhuEd.portal_loginStatus()
                else:
                    gzhuEd.academicSystem_loginStatus()

            driver.switch_to.window(windows[-1])
            gzhuEd.save_cookie()
        except Exception:
            logger.error('Cookie更新失败！')
            logger.error(traceback.format_exc())

            retry = 1
