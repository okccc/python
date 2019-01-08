# coding=utf-8
"""
解决问题：
1.某些标签里的text被内部某个标签割开成了好几段导致xpath无法直接获取,可以用remove_tags适当去除标签方便获取文本
2.requests.exceptions.TooManyRedirects: Exceeded 30 redirects
"""
import requests
from lxml import etree
from bs4 import BeautifulSoup
from w3lib.html import remove_tags
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


def baidu(flag=False):
    # 负面消息关键字
    negative_words = ["110网", "骗", "忽悠", "合法", "征信", "名声", "坑", "违约", "不还", "起诉", "法院", "律师", "正规", "违规", "暴力", "后悔",
                      "反悔"]
    datas = []
    wds = ["美好分期", "美好分趣"]
    for wd in wds:
        if flag:
            for page in range(1, 20):
                pn = (page - 1) * 10
                params = {"wd": wd, "pn": pn}
                parse(datas, negative_words, params)
                time.sleep(1)
        else:
            for page in range(1, 3):
                pn = (page - 1) * 10
                # 设置搜索时间范围：通过fiddler抓包获取WebForms表单参数name/value
                params = {"wd": wd, "pn": pn, "gpc": "stf=1545357558.176,1545962358.175|stftype=1"}
                parse(datas, negative_words, params)
    # 对列表中的字典去重
    return [dict(t) for t in {tuple(d.items()) for d in datas}]


def parse(datas, negative_words, params):
    url = "https://www.baidu.com/s?"
    headers = {
        "User-Agent": "Chrome Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
    }
    response = requests.get(url, params=params, headers=headers)

    # # xpath解析
    # html = etree.HTML(response.text)
    # results = html.xpath("//div[@id='content_left']/div[contains(@class, 'result')]/h3/a")
    # for each in results:
    #     link = each.xpath("./@href")[0]
    #     # 百度反爬虫：搜索的结果都是www.baidu.com域名的重定向跳转链接,需要继续访问跳转链接获取重定向后的url
    #     real_link = ""
    #     if link.startswith("http"):
    #         # requests默认自动处理302跳转,经过跳转的请求返回的url/status_code/headers都是跳转后的信息,可用response.history追踪跳转情况
    #         # 如果请求跳转过多可能会报错：TooManyRedirects: Exceeded 30 redirects 禁用重定向还可以减少网络消耗提高访问速度
    #         response = requests.get(link, headers=headers, allow_redirects=False)
    #         if response.status_code < 400:
    #             # 禁用重定向后status_code是302,通过response.headers["Location"]获取重定向的url
    #             real_link = response.headers["Location"]
    #             if "www.zhihu.com" in real_link:
    #                 real_link = real_link.replace("https", "http")
    #     # 去除碍事标签直接获取文本
    #     title = remove_tags(etree.tostring(each, encoding="utf8").decode("utf8"))
    #     for word in negative_words:
    #         if word in title:
    #             # 有word符合就添加数据
    #             data = {"title": title, "link": real_link}
    #             datas.append(data)
    #             # 结束循环防止一个title多个word重复添加
    #             break

    # bs4解析
    soup = BeautifulSoup(response.text, "lxml")
    for tag in soup.select("h3 > a"):
        # 优点：取标签里的文本时不用去除多余标签就能获取完整text
        title = tag.text
        link = tag.attrs["href"]
        real_link = ""
        if link.startswith("http"):
            response = requests.get(link, headers=headers, allow_redirects=False)
            if response.status_code < 400:
                # 禁用重定向后status_code是302,通过response.headers["Location"]获取重定向的url
                real_link = response.headers["Location"]
                if "www.zhihu.com" in real_link:
                    real_link = real_link.replace("https", "http")
        for word in negative_words:
            if word in title:
                # 有word符合就添加数据
                data = {"title": title, "link": real_link}
                datas.append(data)
                # 结束循环防止一个title多个word重复添加
                break


def test():

    headers = {
        "User-Agent": "Chrome Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
    }
    url = "https://www.baidu.com/link?url=0xKhTSzNJI_G7_jq0Td2If3R4csvpMEXvg_A0IZ7cuB3UuY8TH1uL-yAGSP7Gpm4JIZE-NQdySTvvcq3U3dRb_&amp;wd=&amp;eqid=cd3c51c00004a1c2000000045c270b1c"

    response01 = requests.get(url, headers=headers)
    response02 = requests.get(url, headers=headers, allow_redirects=False)
    print(response01.url)  # http://www.110.com/ask/question-11975553.html
    print(response01.status_code)  # 200
    print(response01.headers)  # {'Transfer-Encoding': 'chunked', 'Server': 'nginx/1.6.2', 'Connection': 'close', 'Vary': 'Accept-Encoding', 'Content-Encoding': 'gzip', 'Date': 'Sat, 29 Dec 2018 08:47:04 GMT', 'Content-Type': 'text/html; charset=utf-8'}
    print(response01.history)  # [<Response [302]>]

    print(response02.url)  # https://www.baidu.com/link?url=0xKhTSzNJI_G7_jq0Td2If3R4csvpMEXvg_A0IZ7cuB3UuY8TH1uL-yAGSP7Gpm4JIZE-NQdySTvvcq3U3dRb_&amp;wd=&amp;eqid=cd3c51c00004a1c2000000045c270b1c
    print(response02.status_code)  # 302
    print(response02.headers)  # {'X-Xss-Protection': '1;mode=block', 'Set-Cookie': 'BDSVRTM=0; path=/', 'Content-Length': '225', 'Date': 'Sat, 29 Dec 2018 08:47:04 GMT', 'Content-Type': 'text/html;charset=utf8', 'Location': 'http://www.110.com/ask/question-11975553.html', 'Pragma': 'no-cache', 'Server': 'BWS/1.1', 'Connection': 'Keep-Alive', 'Expires': 'Fri, 01 Jan 1990 00:00:00 GMT', 'X-Ua-Compatible': 'IE=Edge,chrome=1', 'Cache-Control': 'no-cache, must-revalidate', 'Bdpagetype': '3'}


if __name__ == '__main__':
    # print(baidu())
    test()