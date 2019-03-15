# coding=utf-8
"""
Selenium是一个Web自动化测试工具,会按指定的命令自动操作,可以结合第三方浏览器做网络爬虫,模拟登录操作
Selenium很慢：因为requests只会请求当前url,而Selenium会请求当前url+js+css+img所有这些资源,可以设置chrome不加载图片提升速度
ChromeDriver镜像下载地址 --> https://npm.taobao.org/
注意事项：
selenium获取的页面数据是浏览器中elements的内容
find_element返回一个element,如果没有就会报错,find_elements返回列表,如果没有就是空列表,可根据find_elements结果列表长度判断是否有下一页
如果页面中包含frame/iframe,需要先调用driver.switch_to_frame方法切换到frame中才能定位元素
selenium请求第一页数据时会等待页面加载完,而在点击翻页后是不会等待页面加载完的,直接获取数据可能会报错,需要time.sleep(3)

查看网页源代码(sources)：服务器发送到浏览器的原始内容
查看元素(F12)：经过浏览器渲染,执行js动态生成的内容(如果网站没有使用ajax动态加载其实就等同于源码)
判断页面是否ajax动态加载：
在网页源码里查找页面上的数据信息,搜到说明是正常页面,url地址即真实请求地址(直接抓源码即可)
搜不到说明页面数据是调用了其它接口,F12-->Network-->Headers或者fiddler找到真实请求地址,格式类似xxxAjax.json?key=value(需要抓接口或者selenium模拟浏览器操作)

tesseract是一个将图像翻译成文字的OCR库(optical character recognition) --> 识别验证码效果一般,还是用云打码平台吧
from PIL import Image
import pytesseract
img = Image.open("./test.jpg")
print(pytesseract.image_to_string(img))
"""

from selenium import webdriver  # 导入webdriver
from selenium.webdriver import ActionChains  # 导入行为链
from selenium.webdriver.common.keys import Keys  # 导入keys调用键盘按键
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests

class Selenium01(object):
    def __init__(self):
        # 设置chrome不加载图片,不然打开页面速度有点慢(可选)
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        # 创建浏览器对象
        self.driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe", options=options)

    def introduce(self):
        # 打开百度页面
        self.driver.get("https://www.baidu.com")
        # 设置窗口最大化
        self.driver.maximize_window()
        # 截屏
        self.driver.save_screenshot("./screen.png")
        # 获取input标签 --> webdriver.py模块包含各种定位元素方法
        tag = self.driver.find_element_by_id("kw")
        # 获取标签的某个属性值
        print(tag.get_attribute("class"))  # s_ipt
        # 通过input标签输入内容
        tag.send_keys("lol")
        # 模拟点击
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

    def chains(self):
        # 打开百度页面
        self.driver.get("https://www.baidu.com")
        # 获取输入框标签和提交标签
        tag1 = self.driver.find_element_by_id("kw")
        tag2 = self.driver.find_element_by_id("su")
        # 创建鼠标行为链对象
        ac = ActionChains(self.driver)
        # 操控鼠标
        ac.move_to_element(tag1)
        ac.send_keys_to_element(tag1, "大数据")
        ac.move_to_element(tag2)
        ac.click()
        # 执行上面一系列操作
        ac.perform()
        time.sleep(3)
        # 退出浏览器
        self.driver.quit()

    def wait(self):
        # 注意：selenium的显式等待和隐式等待没什么用,建议直接强制等待time.sleep(5)
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

    def windows(self):
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

    @staticmethod
    def proxy():
        # 使用代理ip
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server-http://124.225.176.82:8010")
        driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe", chrome_options=options)
        driver.get("https://www.baidu.com")

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


if __name__ == '__main__':
    s = Selenium01()
    # s.introduce()
    # s.chains()
    # s.wait()
    # s.windows()
    # s.proxy()
    s.cookie()
