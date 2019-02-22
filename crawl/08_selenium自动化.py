# coding=utf-8
"""
Selenium是一个Web自动化测试工具,可以按指定的命令自动操作,结合第三方浏览器做网络爬虫

查看网页源代码(sources)：服务器发送到浏览器的原始内容
查看元素(F12)：经过浏览器渲染,执行js动态生成的内容(如果网站没有使用ajax动态加载其实就等同于源码)

判断页面是否是ajax动态加载：
在网页源码里查找页面上的数据信息,搜到说明是正常页面,url地址即真实请求地址(直接抓源码即可)
搜不到说明页面数据是调用了其它接口,F12-->Network-->Headers找到真实请求地址,类似xxxAjax.json?***这种格式(需要抓接口或者selenium模拟浏览器操作)
"""

# 导入webdriver
from selenium import webdriver
# 导入keys调用键盘按键
from selenium.webdriver.common.keys import Keys
import time

# 设置chrome不加载图片,不然打开页面速度有点慢(可选)
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# 创建浏览器对象
driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe", chrome_options=chrome_options)

"""
快速入门
"""
def introduce():
    # 打开一个页面
    driver.get("https://www.baidu.com")

    # 获取input标签(webdriver.py模块包含各种定位元素方法)
    tag = driver.find_element_by_id("kw")
    # 获取标签的某个属性值
    print(tag.get_attribute("class"))  # s_ipt
    # 通过input标签输入内容
    tag.send_keys("lol")

    # 模拟点击
    driver.find_element_by_id("su").click()

    # 打印网页渲染后的源码
    print(type(driver.page_source))  # <class 'str'>

    # 获取当前页面cookie
    print(driver.get_cookies())

    time.sleep(3)

    # ctrl a全选输入框内容
    driver.find_element_by_id("kw").send_keys(Keys.CONTROL, "a")

    # ctrl x剪切输入框内容
    driver.find_element_by_id("kw").send_keys(Keys.CONTROL, "x")

    # 输入框重新输入内容
    driver.find_element_by_id("kw").send_keys("云计算")

    # 点击百度一下
    driver.find_element_by_id("su").click()

    time.sleep(3)

    # 清除输入框内容
    driver.find_element_by_id("kw").clear()

    # 获取当前url
    print(driver.current_url)

    time.sleep(3)

    # 关闭当前页面,如果只有一个页面就关闭浏览器
    driver.close()

    # 直接关闭浏览器
    driver.quit()


"""
鼠标行为链
"""
def chains():
    # 需求：在百度搜索大数据

    from selenium.webdriver import ActionChains
    driver.get("https://www.baidu.com")

    # 获取输入框标签和提交标签
    tag1 = driver.find_element_by_id("kw")
    tag2 = driver.find_element_by_id("su")

    # 创建鼠标行为链对象
    ac = ActionChains(driver)

    # 操控鼠标
    ac.move_to_element(tag1)
    ac.send_keys_to_element(tag1, "大数据")

    ac.move_to_element(tag2)
    ac.click()

    # 执行上面一系列操作
    ac.perform()


"""
页面等待
"""
def wait():
    # 1、显示等待：设置等待时长并指定条件(常用)
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    driver.get("https://www.baidu.com")

    try:
        # 循环页面5秒直到id="xxx"出现
        element = WebDriverWait(driver, 5).until(
            # EC后面接指定条件(expected_conditions.py模块包含各种内置等待条件)
            EC.presence_of_element_located((By.ID, "abc"))
        )
        print(element)
    except Exception as e:
        print(e)
    finally:
        driver.quit()

    # 2、隐示等待：只设置等待时长(等同于time.sleep)
    # driver.implicitly_wait(5)
    # driver.find_element_by_id("hehe")


"""
多窗口切换
"""
def windows():
    # 先打开百度页面
    driver.get("https://www.baidu.com")
    # 再打开另一个网页
    # driver.get("https://www.douban.com")  # 直接get会覆盖先前的页面
    driver.execute_script("window.open('https://www.douban.com/')")
    # 此时鼠标还是停留在第一个打开的页面上的
    print(driver.current_url)  # https://www.baidu.com/

    # window_handles按照打开顺序存储窗口
    windows = driver.window_handles
    for window in windows:
        print(window)

    # 切换到指定窗口
    driver.switch_to_window(windows[1])
    print(driver.current_url)  # https://www.douban.com/
    time.sleep(5)
    # 关掉当前页
    driver.close()
    # 再回到初始页面
    driver.switch_to_window(windows[0])


"""
使用代理ip
"""
def proxy():
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server-http://124.225.176.82:8010")
    driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe", chrome_options=options)
    driver.get("https://www.baidu.com")


"""
操作cookie
"""
def cookie():
    driver.get("https://www.baidu.com")
    for cookie in driver.get_cookies():
        print(cookie["domain"])

    print("=" * 50)
    driver.delete_all_cookies()


if __name__ == '__main__':
    introduce()
    # chains()
    # wait()
    # windows()
    # proxy()
    # cookie()
