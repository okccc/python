# coding=utf-8
"""
注意: 使用etree.HTML()时,如果response.encoding不是utf-8后面response.text可能会乱码,这时可以用response.content代替
content = response.content
html = etree.HTML(content)
res_list = html.xpath("***")

报错: SyntaxError: Non-UTF-8 code starting with '\xe5' on line 67, but no encoding declared;
原因: Python默认编码是ASCII,代码中出现中文字符就会报错,在python文件首行加上# coding=utf-8即可
"""

import requests
from lxml import etree
import jieba  # 中文分词器
from collections import Counter  # Counter类用于统计元素个数
from pyecharts import WordCloud


class Chinese(object):
    """
    需求：爬取李克强政府工作报告内容并做词频统计
    """

    def crawl(self):
        # 链接
        url = "http://www.gov.cn/premier/2017-03/16/content_5177940.htm"
        # 请求头
        headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"}
        # 发送get请求
        response = requests.get(url, headers=headers)
        print(response.encoding)  # ISO-8859-1
        # 获取数据
        content = response.content
        # 解析HTML文档
        html = etree.HTML(content)
        print(type(html))  # <class 'lxml.etree._Element'>
        # 使用xpath表达式
        res_list = html.xpath("//p | //span")
        # 调用中文分词处理
        self.participle(res_list)

    def participle(self, text):
        data = ""
        # 遍历列表
        for res in text:
            if res.text is not None:
                data += res.text

        # 1、先做分词
        seg_list = jieba.cut(data, cut_all=True)
        print(type(seg_list))  # <class 'generator'>

        # 读取中文停用词库
        filepath = "D://PycharmProjects/python/analysis/csv/中文停用词库.txt"
        # 将停用词库处理为列表
        stopwords = [line.strip() for line in open(filepath, encoding="utf-8")]
        print(stopwords)

        # 2、停用词处理
        words = [seg for seg in seg_list if seg not in stopwords and seg != ""]
        print(words)

        # 3、词频统计Counter(): 返回Counter({k1: v1, k2: v2, k3: v3...})并按value值降序排序
        counter = Counter(words)
        print(type(counter))  # <class 'collections.Counter'>
        print(counter)  # Counter({'发展': 134, '改革': 85, '经济': 71, '推进': 66...})
        # print(type(counter.keys()))

        # counter.most_common()将Counter({k1: v1, k2: v2...})转换成列表[(k1, v1),(k2, v2)...],参数n相当于topN
        res = counter.most_common(n=10)
        print(type(res))  # <class 'list'>
        print(res)  # [('发展', 134), ('改革', 85), ('经济', 71), ('推进', 66)...]

        # 调用绘制词云图方法
        self.draw(counter)

    def draw(self, counter):
        # 绘制词云图
        wc = WordCloud(title="李克强政府工作报告")
        wc.add("词频统计", counter.keys(), counter.values())
        wc.render("D://PycharmProjects/python/analysis/html/xixi.html")


if __name__ == '__main__':
    c = Chinese()
    c.crawl()