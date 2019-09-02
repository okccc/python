"""
验证码识别
1.简单的图像文字可以用tesseract或CNN神经网络训练数据集预测,再不行就云打码平台
2.极验(滑动)验证码要先计算窗口偏移量大小然后selenium模拟拖动按钮
tesseract是一个将图像翻译成文字的OCR库(optical character recognition) --> 识别验证码效果一般,还是用云打码平台吧
windows安装tesseract-ocr并配置环境变量
from PIL import Image
import pytesseract
img = Image.open("./test.jpg")
# 此处可能需要做降噪和二值化处理,去除干扰线等
print(pytesseract.image_to_string(img))
"""
import requests
import json
from aip import AipOcr
from lxml import etree
import base64
import urllib.request
import urllib.parse
from PIL import Image


class GetCode(object):

    def __init__(self):
        # 创建应用生成的API_Key和Secret_Key
        self.API_Key = "s8GHTluI1Xy1OvM7UU0wx4wl"
        self.Secret_Key = "lnUFZRN05rMYshbmRGcZvYsrZnMbtXro"
        # 获取access_token的url
        self.url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'
        # 识别验证码的url
        self.api = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage?access_token={}"
        self.headers = {
            "Content-Type": 'application/x-www-form-urlencoded'
        }

    def get_access_token(self):
        """获取access_token"""
        response = requests.post(self.url.format(self.API_Key, self.Secret_Key), headers=self.headers)
        access_token = json.loads(response.text)['access_token']
        return access_token

    def get_img_src(self):
        # 网站注册地址
        url = 'https://id.ifeng.com/user/register/'
        response = requests.get(url, headers=self.headers)
        html = etree.HTML(response.text)
        # 图片链接
        img_src = html.xpath('//img[@id="js-mobile-reg-code-pic"]/@src')[0]
        urllib.request.urlretrieve(img_src, './code.jpg')
        return img_src

    def init_table(self, threshold=155):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return table

    def opt_image(self):
        im = Image.open("./code.jpg")
        im = im.convert('L')
        im = im.point(self.init_table(), '1')
        im.save('./code1.jpg')
        return "./code1.jpg"

    def get_file_content(self, file_path):
        with open(file_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            data = {'images': base64_data.decode()}
            decoded_data = urllib.parse.urlencode(data)
            return decoded_data

    def show_code(self):
        image = self.get_file_content(self.opt_image())
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        res = requests.post(self.api.format(self.get_access_token()), headers=headers, data=image)
        print(res.text)

    # def main(self):
    #     APP_ID = '16721750'
    #     API_KEY = 's8GHTluI1Xy1OvM7UU0wx4wl'
    #     SECRET_KEY = 'lnUFZRN05rMYshbmRGcZvYsrZnMbtXro'
    #     client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    #     url = 'https://id.ifeng.com/public/authcode'
    #     # 可选参数
    #     options = {
    #         "language_type": "CHN_ENG",
    #         "detect_direction": "true",
    #     }
    #     # 调用通用文字识别
    #     # code = client.webImage(self.get_file_content(), options)
    #     code = client.enhancedGeneralUrl(self.get_img_src(), options)
    #     print(code)


if __name__ == '__main__':
    gc = GetCode()
    gc.get_img_src()
    gc.show_code()