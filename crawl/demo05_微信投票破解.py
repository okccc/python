# coding=utf-8
"""
需求：微信投票限制只能在微信里投票且每个微信号每天只能投一次
分析：只能在微信投票是通过判断UA是否包含微信内置浏览器MicroMessenger实现,每个微信号每天限投一次是通过判断用户的Cookie值实现
解决：通过fiddler手机数据抓包获取请求url,User-Agent,Cookie,模拟微信发送请求并手动更改Cookie值伪装成不同用户突破只能投一票限制
fiddler配置链接：https://www.cnblogs.com/qinyulin/articles/6843829.html
手机设置HTTP代理后无法上网：通用-->关于本机-->证书信任设置-->针对根证书启用完全信任
"""

import requests


def vote():
    # # 请求地址
    # url = "http://hd.konglongcheng.com.cn/HD2018/EXVote/EXVoteHelper.ashx?action=vote&Id=155"
    # # 请求头
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN",
    #     "Cookie": "comm_hd_cookie=oZCrNjtRiwIwiYmhQ4evBHB7S3zQ" + str(i),
    #     "Referer": "http://hd.konglongcheng.com.cn/HD2018/EXVote/index.aspx?txt=155",
    #     "Host": "hd.konglongcheng.com.cn",
    # }
    # # 发送get请求
    # response = requests.get(url, headers=headers)
    # # 查看响应数据
    # print(response.text)

    # url = "https://mp.weixin.qq.com/mp/appmsg_comment?action=likecomment&uin=777&key=777&pass_ticket=wbKDQIrzg3KCI5lcrn2kk4o1yTbtuVogYtmC1yleKidhZODAL1s5Ew%25252BL1COB14c8&wxtoken=777&devicetype=iOS12.1.2&clientversion=17000125&appmsg_token=992_NqrptBaY4I45xS%252BlT3ccxbw1b5eGv4jxxkMUc2FZvFWsV1ABFecPxVFE5rSs6erwi64SFt276LTcRLrm&x5=0&f=json",
    url = "https://mp.weixin.qq.com/mp/appmsg_comment?action=likecomment&uin=777&key=777&pass_ticket=wbKDQIrzg3KCI5lcrn2kk4o1yTbtuVogYtmC1yleKidhZODAL1s5Ew%252BL1COB14c8&wxtoken=777&devicetype=iOS12.1.2&clientversion=17000125&appmsg_token=992_NqrptBaY4I45xS%2BlT3ccxbw1b5eGv4jxxkMUc2FZvFWsV1ABFecPxVFE5rSs6erwi64SFt276LTcRLrm&x5=0&f=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16C101 MicroMessenger/7.0.1(0x17000120) NetType/WIFI Language/zh_CN",
        "Host": "mp.weixin.qq.com",
        "Origin": "https://mp.weixin.qq.com",
        "Referer": "https://mp.weixin.qq.com/s?__biz=MzUyMjE2MTE0Mw==&mid=2247487327&idx=1&sn=6df996995fc8dbd0d64109dffae57f22&chksm=f9d151c7cea6d8d1a3dc72f14de365db2baf0a83fdd167839517c6f3f3c276332f7140af045b&scene=0&xtrack=1&sessionid=1547632462&subscene=92&clicktime=1547632475&ascene=7&devicetype=iOS12.1.2&version=17000125&nettype=WIFI&abtest_cookie=BAABAAoACwATABQABQAllx4AV5keAJuZHgCdmR4At5keAAAA&lang=zh_CN&fontScale=100&pass_ticket=wbKDQIrzg3KCI5lcrn2kk4o1yTbtuVogYtmC1yleKidhZODAL1s5Ew%2BL1COB14c8&wx_header=1",
        "Cookie": "devicetype=iOS12.1.2; lang=zh_CN; pass_ticket=wbKDQIrzg3KCI5lcrn2kk4o1yTbtuVogYtmC1yleKidhZODAL1s5Ew+L1COB14c8; rewardsn=; version=17000125; wap_sid2=CLbLm/YDElxtSElkODFLZHVUdW9SVm1kY21MLXZDNXcxOC1nVEliYTBqb0xLSndlOHpuTHp4RmFSZWRZUTk4aXRjYko0RE01MjdjODU5aGlFSjZXdWlINVRVSkhSLUFEQUFBfjCdhvzhBTgNQAE=; wxtokenkey=777; wxuin=1053222326; pgv_pvid=5661142221; ts_uid=3005708013; _scan_has_moon=1; pgv_pvid_new=085e9858ed6d664b05f8f0fce@wx.tenpay.com_6e8a5dc79c"
    }
    data = {
        "action": "likecomment",
        "appmsg_token": "992_NqrptBaY4I45xS%2BlT3ccxbw1b5eGv4jxxkMUc2FZvFWsV1ABFecPxVFE5rSs6erwi64SFt276LTcRLrm",
        "key": 777,
        "uin": 777,
        "wxtoken": 777,
        "like": 1,
        "__biz": "MzUyMjE2MTE0Mw==",
        "appmsgid": 2247487327,
        "comment_id": 627588963393601536,
        "content_id": 4523555445587050497,
        "item_show_type": 0,
        "scene": 0
    }
    # response = requests.get(url, headers=headers)
    response = requests.post(url=url, data=data, headers=headers)
    print(response.text)


if __name__ == '__main__':
    vote()