import json

import selenium.webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def wd_login(driver_path, xuhao, mima):
    edge = {
        "ms:edgeOptions": {
            'excludeSwitches': ['enable-automation', 'enable-logging'],
            'args': ['--headless', '--disable-gpu']
        }
    }

    driver = selenium.webdriver.Edge(driver_path, capabilities=edge)

    driver.get(
        f'https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fnewmy.gzhu.edu.cn%2Fup%2Fview%3Fm%3Dup'
    )

    try:
        # 智能等待
        WebDriverWait(driver, 10, 0.5).until(
            ec.visibility_of_element_located((By.ID, 'un')))
    except:
        pass

    driver.find_element_by_id('un').send_keys(xuhao)
    driver.find_element_by_id('pd').send_keys(mima)
    driver.find_element_by_id('index_login_btn').click()

    try:
        WebDriverWait(driver, 10, 0.5).until(
            ec.visibility_of_element_located(
                (By.XPATH,
                 '//img[@src="/up/resource/image/home/gz/app/jwxt.png"]')))
    except:
        pass

    yield driver

    title = driver.title
    if title == '融合门户':
        driver.close()
        windows = driver.window_handles
        driver.switch_to_window(windows[0])

    try:
        WebDriverWait(driver, 10, 0.5).until(
            ec.visibility_of_element_located((By.XPATH, '//span[@id="xtmc"]')))
    except:
        pass

    driver.find_element_by_xpath(
        '//nav[@id="cdNav"]/ul[@class="nav navbar-nav"]/li[3]').click()
    driver.find_element_by_xpath('//a[contains(text(),"自主选课")]').click()

    title = driver.title
    if title == '广州大学教学综合信息服务平台':
        driver.close()
        windows = driver.window_handles
        driver.switch_to_window(windows[0])

    try:
        WebDriverWait(driver, 10, 0.5).until(
            ec.visibility_of_element_located(
                (By.XPATH, '//div[@class="navbar-header"]')))
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

    yield driver
