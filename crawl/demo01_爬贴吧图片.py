# coding=utf-8
import urllib.parse
import urllib.request
import random
from lxml import etree


class TieBa01(object):
    def __init__(self, kw):
        self.url = "https://tieba.baidu.com/f?kw={}&pn={}&ie=utf-8"
        self.kw = kw
        self.ua_list = [
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"},
        ]

    def get_url(self):
        # 对贴吧名称做url转码
        kw = urllib.parse.urlencode({"kw": self.kw})
        return [self.url.format(kw, (i-1)*50) for i in range(1, 1000)]

    def get_data(self, url):
        # 创建请求对象
        request = urllib.request.Request(url, headers=random.choice(self.ua_list))
        # 发送请求,接受响应
        data = urllib.request.urlopen(request).read()
        return data

    def main(self):
        # 1.获取url列表
        urls = self.get_url()
        # 2.发送请求,获取响应
        for url in urls:
            self.get_data(url)
        # 3.解析数据

        # 4.保存数据


if __name__ == "__main__":
    tb = TieBa01(input("请输入贴吧名称："))
    tb.main()
