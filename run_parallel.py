# coding=utf-8
# auther：lucas
# date：2019/7/12 10:50
# tools：PyCharm
# Python：3.7.3
import threading
from selenium import webdriver
import time


caps = {'platform': 'ANY',
        'browserName': None,
        'version': '',
        # "enableVNC": True,
        # 'javascriptEnabled': True,
        'recordVideo': True,
        'build': "build_%s" % time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()),
        'name': 'test_%s' % time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()),
        'idleTimeout': 90,
        'screenResolution': '1280x720',
        # 'tz': 'Asia/Shanghai',
        # 'tz': 'America/Montreal',
        'testFileNameTemplate': '{platform}_{browser}_{testStatus}_{timestamp}',
        # 'name': 'my_test_name',
        }


def run_browser(browser="chrome"):
    if browser.lower() == "chrome":
        caps['browserName'] = "chrome"
    if browser.lower() == "firefox":
        caps['browserName'] = "firefox"
    # print(caps)
    dr = webdriver.Remote('http://localhost:4444/wd/hub', desired_capabilities=caps)
    dr.get("https://www.baidu.com")
    dr.add_cookie({"name": "zaleniumMessage", "value": "go to baidu page"})
    dr.add_cookie({"name": "zaleniumMessage", "value": "input keyword"})
    dr.find_element_by_id("kw").send_keys("zalenium")
    dr.add_cookie({"name": "zaleniumMessage", "value": "click search button"})
    dr.find_element_by_id("su").click()
    print(dr.find_element_by_id("su").is_displayed())


threads = []
temp_thrad = threading.Thread(target=run_browser, args=())
temp_thrad1 = threading.Thread(target=run_browser, args=("firefox",))
threads.append(temp_thrad)
threads.append(temp_thrad1)
for t in threads:
    t.setDaemon(True)
    t.start()
for i in threads:
    i.join()

