![在这里插入图片描述](https://img-blog.csdnimg.cn/20190710160742553.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xiMjQ1NTU3NDcy,size_16,color_FFFFFF,t_70)
##### 简介
[Zalenium](https://opensource.zalando.com/zalenium/) 是一个Selenium Grid的扩展，它使用[docker-selenium](https://github.com/elgalu/docker-selenium)在本地运行基于Firefox和Chrome的测试，同样带有视频录制，实时预览，基本认证和仪表盘等功能；如果需要其他的浏览器，则需要用到云测试提供商（Sauce Labs，BrowserStack，TestingBot），当然这些是收费的。。。不过好在Firefox和Chrome是开源的，基本已经够用了。 Zalenium也可以在Kubernetes中使用。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190712135607766.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xiMjQ1NTU3NDcy,size_16,color_FFFFFF,t_70)
##### 安装
###### 前置条件
- [Docker](https://docs.docker.com/docker-for-windows/) version >= 1.11.1（可能适用于低版本，没有测试过）
- 运行 `docker info`不会报错

###### 下载镜像

    docker pull elgalu/selenium
    docker pull dosel/zalenium
下载成功后运行：
```
docker run --rm -ti --name zalenium -p 4444:4444 -v /var/run/docker.sock:/var/run/docker.sock -v /temp/videos:/home/seluser/videos   --privileged dosel/zalenium start
```
默认只启动一个chrome container和一个Firefox container，如需启动多个则运行（添加参数`--desiredContainers 4`）：
```
docker run --rm -ti --name zalenium -p 4444:4444 -v /var/run/docker.sock:/var/run/docker.sock -v /temp/videos:/home/seluser/videos   --privileged dosel/zalenium start --desiredContainers 4
```
查看zalenium的参数用`-h  --help`:

```
docker run --rm -ti --name zalenium -p 4444:4444 -v /var/run/docker.sock:/var/run/docker.sock -v /temp/videos:/home/seluser/videos   --privileged dosel/zalenium start -h
```

等待zalenium准备，调用：http://localhost:4444/wd/hub/status 你将会看到类似如下返回值：

```json
{
  "status": 0,
  "value": {
    "ready": true,
    "message": "Hub has capacity",
    "build": {
      "revision": "unknown",
      "time": "unknown",
      "version": "3.141.59"
    },
    "os": {
      "arch": "amd64",
      "name": "Linux",
      "version": "4.9.125-linuxkit"
    },
    "java": {
      "version": "1.8.0_212"
    }
  }
}
```

然后你将会看到：

- 命令行窗口
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190712140257501.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xiMjQ1NTU3NDcy,size_16,color_FFFFFF,t_70)
- Grid: http://localhost:4444/grid/console
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190712140856830.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xiMjQ1NTU3NDcy,size_16,color_FFFFFF,t_70)
- 实时预览：http://localhost:4444/grid/admin/live，可以增加 `?refresh=numberOfSeconds`，自动刷新页面，例如：http://localhost:4444/grid/admin/live?refresh=20；`?build=myTestBuild`，查看单个构建，例如：http://localhost:4444/grid/admin/live?build=myTestBuild
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190712140925516.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xiMjQ1NTU3NDcy,size_16,color_FFFFFF,t_70)
- Dashboard：http://localhost:4444/dashboard/#
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190712141002389.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xiMjQ1NTU3NDcy,size_16,color_FFFFFF,t_70)

或者可以用Docker Compose启动zalenium，`docker-compose.yml`样例：

```yaml
    # Usage:
    #   docker-compose up --force-recreate
    version: '2.1'
    
    services:
      #--------------#
      zalenium:
        image: "dosel/zalenium"
        container_name: zalenium
        hostname: zalenium
        tty: true
        volumes:
          - /tmp/videos:/home/seluser/videos
          - /var/run/docker.sock:/var/run/docker.sock
         # - /usr/bin/docker:/usr/bin/docker
        ports:
          - 4444:4444
        command: >
          start --desiredContainers 2
                --maxDockerSeleniumContainers 8
                --screenWidth 800 --screenHeight 600
                --timeZone "Europe/Berlin"
                --videoRecordingEnabled true
                --sauceLabsEnabled false
                --browserStackEnabled false
                --testingBotEnabled false
                --cbtEnabled false
                --startTunnel false
        environment:
          - HOST_UID
          - HOST_GID
```
创建`docker-compose.yml`文件后，该文件目录下运行：`docker-compose up`
即可看到上文描述的结果。
##### 测试配置选项

```python
caps = {'platform': 'ANY',
        'browserName': "chrome",
        'version': '',
        # 是否录制视频
        'recordVideo': True,
        # build 名字
        'build': "my_build_name123",
        # 测试名称
        'name': 'my_test_name123',
        # 超时时间
        'idleTimeout': 90,
        # 分辨率
        'screenResolution': '1280x720',
        # 时区
        # 'tz': 'Asia/Shanghai',
        # 视频文件名称
        'testFileNameTemplate': '{platform}_{browser}_{testStatus}_{timestamp}',
        }
# 标记测试成功、失败
driver.add_cookie({"name": "zaleniumTestPassed", "value": "true"})
# 每一步在视频中添加注释
driver.add_cookie({"name": "zaleniumMessage", "value": "go to baidu page"})
```

##### 运行用例
-  Python环境
- `pip insatll -U selenium`

安装完毕后，运行脚本：

```python
# coding=utf-8
# auther：lucas
# date：2019/7/1 17:40
# tools：PyCharm
# time zone: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
import unittest
from selenium import webdriver


class MyTestCase(unittest.TestCase):

    def setUp(self):
        ds = {'platform': 'ANY',
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
        self.dr = webdriver.Remote('http://localhost:4444/wd/hub', desired_capabilities=ds)

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
```
运行完将会通过上面的[Dashboard](http://localhost:4444/dashboard/#)和[实时预览](http://localhost:4444/grid/admin/live)即可看到结果（视频可能需要等一下才可以生成）
关于并发的脚本：

```python
# coding=utf-8
# auther：Liul5
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
```
将会看到结果（同时运行两个浏览器）：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190712143211724.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xiMjQ1NTU3NDcy,size_16,color_FFFFFF,t_70)

##### 参考
- GitHub： https://github.com/zalando/zalenium
- 官网：https://opensource.zalando.com/zalenium/
- https://devopsqa.wordpress.com/2018/11/20/zalenium-docker-selenium-grid/
- https://dev.to/bufferings/tried-zalenium-to-run-selenium-tests-on-scalable-containers-2n7c
- http://www.testautomationguru.com/selenium-webdriver-disposable-selenium-grid-infrastructure-setup-using-zalenium/
- https://medium.com/@tuliobluz/zalenium-brief-introduction-with-protractor-5d9e4f5f85cb
- https://automationcalling.com/2018/07/09/cross-browser-parallel-automation-test-on-local-remote-and-cloud-using-zalenium/
