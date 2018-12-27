# coding=utf-8
"""
问题：某些标签里的text被内部某个标签割开成了好几段导致xpath无法直接获取,可以用remove_tags适当去除标签方便获取文本
"""
import requests
from lxml import etree
from w3lib.html import remove_tags
import jieba
import time
import urllib.request


def baidu_mhfq():
    title_words = ["110网","骗","忽悠","征信","合法","名声","坑","违约","不还","起诉","法院","律师","正规","违规","暴力","后悔","反悔"]
    datas = []
    for page in range(1, 10):
        pn = (page - 1) * 10
        url = "https://www.baidu.com/s?"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"}
        params = {"wd": "美好分期", "pn": pn}
        response = requests.get(url, params=params, headers=headers)
        html = etree.HTML(response.text)
        results = html.xpath("//div[@id='content_left']/div[contains(@class, 'result')]/h3/a")
        for each in results:
            link = each.xpath("./@href")[0]
            title = remove_tags(etree.tostring(each, encoding="utf8").decode("utf8"))
            title_list = jieba.cut_for_search(title)
            for each in title_list:
                if each in title_words:
                    data = {"title": title, "link": link}
                    datas.append(data)
        time.sleep(1)
    return datas


def test():
    # url = "http://www.baidu.com/link?url=DXRAg_8k5tClVZlr6m2Lwcq_BijDyknUaC6bR3DmWnjQxDG_iLi8C03EteI5_CX3qpohxYLR2vbsMZjWvHkKo_"
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17"}
    # # response = urllib.request.urlopen(urllib.request.Request(url, headers=headers))
    # response = requests.get(url, headers=headers)
    # print(response.url)

    l = [{"title": "aaa", "link": "111"},{"title": "bbb", "link": "111"},{"title": "aaa", "link": "111"}]
    new_l = [dict(t) for t in {tuple(d.items()) for d in l}]
    print(new_l)


if __name__ == '__main__':
    # res = baidu_mhfq()
    # print(res)
    test()