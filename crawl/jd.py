import cv2
import time
import numpy as np
from selenium import webdriver
import urllib.request
from selenium.webdriver.common.action_chains import ActionChains


# 设置chrome不加载图片,不然打开页面速度有点慢(可选)
options = webdriver.ChromeOptions()
# 1: 允许加载全部图片  2: 禁止加载全部图片  3: 禁止加载第三方图片
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
# 创建浏览器对象
driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe", options=options)
# 创建鼠标行为链对象
ac = ActionChains(driver)
url = 'https://passport.jd.com/new/login.aspx?'

def jd_login():
    # 打开京东登录页面
    driver.get(url)
    time.sleep(5)
    # 切换到账户登录(注意：切换后html标签会添加属性class="checked"表示当前选项被选中)
    driver.find_element_by_xpath('//div[contains(@class,"login-tab-r")]/a').click()
    # 输入账号密码并点击登录
    driver.find_element_by_name('loginname').send_keys('***')
    driver.find_element_by_name('nloginpwd').send_keys('***')
    driver.find_element_by_id('loginsubmit').click()
    time.sleep(5)
    while True:
        try:
            res = slide()
            if res:
                break
        except Exception as e:
            print(e)

def slide():
    # 滑块图和背景大图的链接
    back_img_url = driver.find_element_by_xpath('//div[@class="JDJRV-bigimg"]/img').get_attribute('src')
    slide_img_url = driver.find_element_by_xpath('//div[@class="JDJRV-smallimg"]/img').get_attribute('src')
    # 下载滑块图和背景图到本地
    back_img, slide_img = 'back.png', 'slide.png'
    urllib.request.urlretrieve(back_img_url, back_img)
    urllib.request.urlretrieve(slide_img_url, slide_img)
    time.sleep(5)
    # 读取图片并灰度化
    block = cv2.imread(slide_img, 0)
    template = cv2.imread(back_img, 0)
    # 保存二值化后的图片
    blockName, templateName = 'block.jpg', 'template.jpg'
    cv2.imwrite(blockName, block)
    cv2.imwrite(templateName, template)
    block = cv2.imread(blockName)
    block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)
    block = abs(255 - block)
    cv2.imwrite(blockName, block)
    block = cv2.imread(blockName)
    template = cv2.imread(templateName)
    # 获取偏移量,查找block在template中的位置,返回结果是一个矩阵,是每个点的匹配结果
    result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)
    print("x方向的偏移", int(y * 0.4 + 18), 'x:', x, 'y:', y)
    # 获取滑块标签
    element = driver.find_element_by_xpath('//div[@class="JDJRV-smallimg"]/img')
    ac.click_and_hold(on_element=element).perform()
    ac.move_to_element_with_offset(to_element=element, xoffset=y, yoffset=0).perform()
    ac.release(on_element=element).perform()
    time.sleep(5)
    url_current = driver.current_url()
    if url_current != url:
        return 0


if __name__ == '__main__':
    jd_login()