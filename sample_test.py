# coding=utf-8
# auther：lucas
# date：2019/7/1 17:40
# tools：PyCharm
# Python：3.7.3
# time zone: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
import unittest
from selenium import webdriver


class MyTestCase(unittest.TestCase):

    def setUp(self):
        caps = {'platform': 'ANY',
              'browserName': "chrome",
              'version': '',
              'recordVideo': True,
              'build': "my_build_name123",
              'name': 'my_test_name123',
              'idleTimeout': 90,
              'screenResolution': '1280x720',
              # 'tz': 'Asia/Shanghai',
              'testFileNameTemplate': '{platform}_{browser}_{testStatus}_{timestamp}',
              }
        self.dr = webdriver.Remote('http://localhost:4444/wd/hub', desired_capabilities=caps)

    def test_something(self):
        self.dr.get("https://www.baidu.com")
        self.dr.add_cookie({"name": "zaleniumMessage", "value": "go to baidu page12"})

        self.assertEqual(self.dr.name, "chrome")

    def test_search_button(self):
        self.dr.get("https://www.baidu.com")
        self.dr.add_cookie({"name": "zaleniumMessage", "value": "go to baidu page"})
        self.dr.add_cookie({"name": "zaleniumMessage", "value": "input keyword"})
        self.dr.find_element_by_id("kw").send_keys("zalenium")
        self.dr.add_cookie({"name": "zaleniumMessage", "value": "click search button"})
        self.dr.find_element_by_id("su").click()
        self.assertTrue(self.dr.find_element_by_id("su").is_displayed())

    def tearDown(self):
        print(self.dr.get_cookies())
        self.dr.add_cookie({"name": "zaleniumTestPassed", "value": "true"})
        self.dr.quit()


if __name__ == '__main__':
    unittest.main()
