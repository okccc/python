# coding=utf-8
"""
错误: 92行--UnicodeEncodeError: 'gbk' codec can't encode character '\ue415' in position 275: illegal multibyte sequence
原因: windows文件默认gbk编码,Python解释器会用gbk编码去解析爬取的网络数据流data,然而此时data是已经decode过的Unicode编码,导致报错
解决方案: 使用open()函数时,应该指定参数encoding='utf-8'
"""

import requests
from lxml import etree
import json
import chardet
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class Qiu(object):
    """
    获取糗事百科每个帖子里的用户头像链接、用户姓名、段子内容、点赞次数和评论次数并保存到json文件
    """

    def getUrl(self, begin, end):
        # 糗事百科URL前面部分
        url = "https://www.qiushibaike.com/8hr/page/"
        # 循环爬取页面
        for page in range(begin, end + 1):
            # 完整URL
            full_url = url + str(page)
            print(full_url)
            # 调用加载页面方法
            self.loadPage(full_url)

    @staticmethod
    def loadPage(url):
        # 请求头
        headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"}
        # 发送get请求
        response = requests.get(url, headers=headers)
        # 查看网页字符编码
        print(response.encoding)  # UTF-8
        # 获取数据
        text = response.text
        # print(type(text))  # <class 'str'>
        # print(text)
        # content = response.content
        # print(type(content))  # <class 'bytes'>
        # print(content)

        # 解析HTML文档为HTML DOM(XML)模型
        html = etree.HTML(text)
        # 返回所有段子的节点位置,contains()模糊查询: 第一个参数是要匹配的标签,第二个参数是标签名的部分内容
        node_list = html.xpath('//div[contains(@id, "qiushi_tag")]')
        # print(node_list)
        # print(type(node_list))  # <class 'list'>

        # 遍历列表
        for node in node_list:
            # 用户头像链接(xpath表达式返回的是list,根据索引取数据)
            imgurl = node.xpath('.//div[@class="author clearfix"]//img/@src')[0]
            # 用户姓名
            username = node.xpath('.//div[@class="author clearfix"]//h2')[0].text.replace('\n', '')
            # 段子内容
            content = node.xpath('.//div[@class="content"]/span')[0].text.replace('\n', '')
            # 点赞次数
            vote = node.xpath('.//span[@class="stats-vote"]/i')[0].text
            # 评论次数
            comments = node.xpath('.//span[@class="stats-comments"]//i')[0].text
            # 往字典添加数据
            item = {
                "imgurl": imgurl,
                "username": username,
                "content": content,
                "vote": vote,
                "comments": comments
            }

            # 写入本地文件
            with open('D://qiubai.json', 'a', encoding='utf-8') as f:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    # 用户输入信息
    begin_page = int(input("输入起始页: "))
    end_page = int(input("输入结束页: "))
    q = Qiu()
    q.getUrl(begin_page, end_page)
