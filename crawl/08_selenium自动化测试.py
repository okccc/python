# coding=utf-8
"""
Selenium是一个自动化测试工具,能够驱动浏览器模拟 输入/点击/跳转/下拉 等操作来拿到网页渲染之后的结果
可以解决requests无法直接执行JS的问题,有些反爬很变态的网站也可以考虑使用selenium + chromedriver
Selenium很慢：因为requests只会请求当前url,而Selenium会请求当前url+js+css+img所有这些资源,可以设置chrome不加载图片提升速度
ChromeDriver镜像下载地址 --> https://npm.taobao.org/
注意事项：
1.selenium获取的页面数据是浏览器渲染过的elements
2.selenium获取标签文本不是tag/text()而是tag.text,获取标签属性不是tag/@href而是tag.get_attribute()
3.find_element()返回第一个标签,没有值会报错,find_elements()返回标签列表,没有值就是空列表 --> 判断下一页用find_elements()
4.如果页面中包含frame/iframe,需要先调用driver.switch_to_frame(0)切换到frame中才能定位元素
5.selenium在提交表单或点击下一页等操作时必须等待页面加载完才能获取数据,不然报错：element is not attached to the page document

查看网页源代码(view-source)：服务器发送到浏览器的原始内容
检查(F12)：elements是经过浏览器渲染执行js动态生成的内容elements=html+js+css+img
爬虫分两种：
1.爬源码：在view-source查找页面上的数据,有说明是静态html页面,地址栏url就是真实请求地址(抓源码)
2.爬接口：没有说明是js/ajax实现的动态html页面,F12-->Network-->Headers或者fiddler抓包(抓ajax请求或者selenium模拟浏览器)
抓包技巧：
1.有些网站pc端数据很难获取(加密、反爬...)可以尝试app端(Toggle device toolbar),很多直接返回json数据
2.在Network查找ajax请求地址时,类似get***?或者***?callback=jsonp/jQuery这种格式的请求会返回json数据
url = "https://i.meituan.com/beauty/medical/channel/shop/ajax/getshops?cityid=1&pageno=3&tagid=1&..."
url = "https://tousu.sina.com.cn/api/index/s?callback=jQuery&keywords=%E4%B8%8A%E6%B5%B7&page_size=10&page=1&..."
url = "https://m.douban.com/movie_showing/items?os=android&for_mobile=1&callback=jsonp2&start=18&count=18&..."
上述url中的callback=jQuery/jsonp2、末尾的时间戳、类似&...这些参数都可以忽略(参考Network-->Headers-->Query String Parameters)
"""

import time

import requests
from selenium import webdriver  # 导入webdriver
from selenium.webdriver import ActionChains  # 导入行为链
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # 导入keys调用键盘按键
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Selenium01(object):
    def __init__(self):
        # 设置chrome不加载图片,不然打开页面速度有点慢(可选)
        options = webdriver.ChromeOptions()
        # 1: 允许加载全部图片  2: 禁止加载全部图片  3: 禁止加载第三方图片
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 创建浏览器对象
        self.driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe", options=options)

    def introduce(self):
        """基本操作"""
        # 打开百度页面
        self.driver.get("https://www.baidu.com")
        # 设置窗口最大化
        self.driver.maximize_window()
        # 截屏
        self.driver.save_screenshot("./screen.png")
        # 有些网站页面加载缓慢,强制等待一下不然获取不到数据
        time.sleep(3)
        # 获取输入框的input标签 --> webdriver.py模块包含各种定位元素方法
        tag = self.driver.find_element_by_id("kw")
        # 获取标签的某个属性值
        print(tag.get_attribute("class"))  # s_ipt
        # 通过input标签输入内容
        tag.send_keys("lol")
        # 获取点百度一下按钮的input标签并点击
        self.driver.find_element_by_id("su").click()
        # 打印浏览器渲染后的网页elements
        print(type(self.driver.page_source))  # <class 'str'>
        # 获取当前页面cookie
        print(self.driver.get_cookies())
        time.sleep(3)
        # ctrl a全选输入框内容
        self.driver.find_element_by_id("kw").send_keys(Keys.CONTROL, "a")
        # ctrl x剪切输入框内容
        self.driver.find_element_by_id("kw").send_keys(Keys.CONTROL, "x")
        # 输入框重新输入内容
        self.driver.find_element_by_id("kw").send_keys("魔兽争霸")
        # 点击百度一下
        self.driver.find_element_by_id("su").click()
        time.sleep(3)
        # 清除输入框内容
        self.driver.find_element_by_id("kw").clear()
        # 获取当前url
        print(self.driver.current_url)
        # 关闭当前页面,如果只有一个页面就关闭浏览器
        self.driver.close()
        # 退出浏览器
        self.driver.quit()

    def windows(self):
        """打开新窗口"""
        # 先打开百度页面
        self.driver.get("https://www.baidu.com")
        # 再打开另一个网页
        # self.driver.get("https://www.douban.com")  # 直接get会覆盖先前的页面
        self.driver.execute_script("window.open('https://www.douban.com/')")
        # 此时鼠标还是停留在第一个打开的页面上的
        print(self.driver.current_url)  # https://www.baidu.com/
        # window_handles按照打开顺序存储窗口
        windows = self.driver.window_handles
        for window in windows:
            print(window)
        # 切换到指定窗口
        self.driver.switch_to_window(windows[1])
        print(self.driver.current_url)  # https://www.douban.com/
        time.sleep(3)
        # 关掉当前页
        self.driver.close()
        # 再回到初始页面
        self.driver.switch_to_window(windows[0])
        # 退出浏览器
        self.driver.quit()

    def login(self):
        """模拟登录"""
        # 打开豆瓣
        self.driver.get('https://www.douban.com/')
        time.sleep(3)
        # 登录表单是在iframe框架里面,先切换到iframe框架,不然无法定位元素  Unable to locate element: {...}
        self.driver.switch_to.frame(0)
        # 切换到密码登录
        self.driver.find_element_by_class_name('account-tab-account').click()
        time.sleep(1)
        # 输入用户名密码
        self.driver.find_element_by_id('username').send_keys('***')
        self.driver.find_element_by_id('password').send_keys('***')
        # 点击登录按钮
        self.driver.find_element_by_xpath('//a[contains(@class, "btn")]').click()
        time.sleep(3)
        # 截屏看是否登录成功
        self.driver.save_screenshot('./aaa.png')
        # 退出浏览器
        self.driver.quit()

    def chains(self):
        """鼠标行为链"""
        # 创建鼠标行为链对象
        ac = ActionChains(self.driver)
        # # 打开页面
        # self.driver.get("https://www.baidu.com")
        # # 获取输入框标签和提交标签
        # tag1 = self.driver.find_element_by_id("kw")
        # tag2 = self.driver.find_element_by_id("su")
        # # 操控鼠标
        # ac.move_to_element(tag1).send_keys("lol")
        # ac.move_to_element(tag2).click()
        # 打开京东
        self.driver.get('https://passport.jd.com/new/login.aspx?')
        time.sleep(3)
        # 切换到账户登录(注意：切换后html标签会添加属性class="checked"表示当前选项被选中)
        self.driver.find_element_by_xpath('//div[contains(@class,"login-tab-r")]/a').click()
        # 输入账号密码并点击登录
        self.driver.find_element_by_name('loginname').send_keys('***')
        self.driver.find_element_by_name('nloginpwd').send_keys('***')
        self.driver.find_element_by_id('loginsubmit').click()
        # 执行上面一系列操作
        ac.perform()
        # time.sleep(3)
        # 退出浏览器
        # self.driver.quit()

    def scroll(self):
        """控制滚动条"""
        # 打开页面
        self.driver.get("https://i.meituan.com/cosmetology/wiki.html?tagid=2")
        time.sleep(3)
        # 获取body对象高度的js
        js1 = 'return document.body.scrollHeight'
        # 下拉滚动条的js
        js2 = 'window.scrollTo(0, document.body.scrollHeight)'
        # 先手动往下拉一下,不然while循环条件不成立
        self.driver.execute_script(js2)
        time.sleep(3)
        # 记录初始高度和循环次数
        old_scroll_height, count = 0, 0
        # 只要往下拉body高度发生变化说明还没到底
        while self.driver.execute_script(js1) > old_scroll_height:
            # 给高度重新赋值
            old_scroll_height = self.driver.execute_script(js1)
            print(old_scroll_height)
            # 继续往下拉
            self.driver.execute_script(js2)
            time.sleep(1)
            count += 1
        # 统计下拉次数
        print(count)
        # 退出浏览器
        self.driver.quit()

    def cookie(self):
        # 打开百度页面
        self.driver.get("https://www.baidu.com")
        # 获取cookie值
        cookies = self.driver.get_cookies()
        print(cookies)
        # 字典生成式获取dict格式的cookies
        cookies = {i["name"]: i["value"] for i in cookies}
        print(cookies)
        # 获取网站的cookie之后可以交给requests使用,因为requests速度比selenium快很多
        requests.get(url="...", cookies=cookies)
        # 删除所有cookie
        self.driver.delete_all_cookies()
        # 退出浏览器
        self.driver.quit()

    def wait(self):
        # selenium的显式等待和隐式等待没什么用,建议直接强制等待time.sleep(5)
        self.driver.get("https://www.baidu.com")
        try:
            # 显式等待：设置等待时长并指定条件(常用) ---> 循环页面5秒直到id="xxx"出现
            element = WebDriverWait(self.driver, 5).until(
                # EC后面接指定条件 --> expected_conditions.py模块包含各种内置等待条件
                EC.presence_of_element_located((By.ID, "abc"))
            )
            print(element)
        except Exception as e:
            print(e)
        finally:
            self.driver.quit()

        # 隐式等待：只设置等待时长(等同于time.sleep)
        # driver.implicitly_wait(5)
        # driver.find_element_by_id("hehe")

    @staticmethod
    def proxy():
        # 使用代理ip
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server-http://124.225.176.82:8010")
        driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe", chrome_options=options)
        driver.get("https://www.baidu.com")


if __name__ == '__main__':
    s = Selenium01()
    # s.introduce()
    # s.windows()
    # s.login()
    s.chains()
    # s.scroll()
    # s.cookie()
    # s.wait()
    # s.proxy()
