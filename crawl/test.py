# coding=utf-8
"""
问题：某些标签里的text被内部某个标签割开成了好几段导致xpath无法直接获取,可以用remove_tags适当去除标签方便获取文本
"""
import requests
from lxml import etree
from w3lib.html import remove_tags
import jieba


def baidu():
    # 负面消息关键字
    negative_words = ["110网", "骗", "忽悠", "合法", "征信", "名声", "坑", "违约", "不还", "起诉", "法院", "律师", "正规", "违规", "暴力", "后悔",
                      "反悔"]
    datas = []
    for page in range(1, 10):
        pn = (page - 1) * 10
        url = "https://www.baidu.com/s?"
        headers = {"User-Agent": "Chrome Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
        params = {"wd": "美好分期", "pn": pn}
        response = requests.get(url, params=params, headers=headers)
        html = etree.HTML(response.text)
        results = html.xpath("//div[@id='content_left']/div[contains(@class, 'result')]/h3/a")
        for each in results:
            link = each.xpath("./@href")[0]
            # 百度搜索的条目都是www.baidu.com域名的地址,点击后会跳转到真实地址,需要再次发送请求获取搜索结果的真实url
            real_link = ""
            if link.startswith("http"):
                real_link = requests.get(link, headers=headers, allow_redirects=False).url
            # 去除碍事标签直接获取文本
            title = remove_tags(etree.tostring(each, encoding="utf8").decode("utf8"))
            # 中文分词
            words = jieba.cut_for_search(title)
            for word in words:
                if word in negative_words:
                    # 有word符合就添加数据
                    data = {"title": title, "link": real_link}
                    datas.append(data)
                    # 结束循环防止一个title多个word重复添加
                    break
    return [dict(t) for t in {tuple(d.items()) for d in datas}]


def test():
    l = [{"title": "aaa", "link": "111"},{"title": "bbb", "link": "111"},{"title": "aaa", "link": "111"}]
    # new_l = [dict(t) for t in {tuple(d.items()) for d in l}]
    # print(new_l)
    print({tuple(d.items()) for d in l})


if __name__ == '__main__':
    print(baidu())
    # test()