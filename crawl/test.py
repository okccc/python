# coding=utf-8
import requests
from lxml import etree
from w3lib.html import remove_tags
import time


def baidu_mhfq():
    datas = []
    wd = input("请输入搜索关键字：")
    for page in range(1, 10):
        pn = (page - 1) * 10
        url = "https://www.baidu.com/s?"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"}
        params = {"wd": wd, "pn": pn}
        response = requests.get(url, params=params, headers=headers)
        html = etree.HTML(response.text)
        results = html.xpath("//div[@id='content_left']/div[contains(@class, 'result')]/h3/a")
        for each in results:
            title = remove_tags(etree.tostring(each, encoding="utf8").decode("utf8"))
            link = each.xpath("./@href")[0]
            data = {"title": title, "link": link}
            datas.append(data)
        time.sleep(2)
    return datas


if __name__ == '__main__':
    res = baidu_mhfq()
    print(res)