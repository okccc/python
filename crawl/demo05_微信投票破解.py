# coding=utf-8
import requests


def vote():
    """
    需求：微信投票限制只能在微信里投票,且每个微信号每天只能投一次
    分析：1.只能在微信投票是通过判断UA是否包含微信内置浏览器MicroMessenger实现
         2.每个微信号每天限投一次是通过判断用户的Cookie值实现
    解决：通过fiddler手机数据抓包获取请求url、User-Agent、Cookie信息,模拟微信发送请求并手动更改Cookie值伪装成不同用户投票
    fiddler配置链接：https://www.cnblogs.com/qinyulin/articles/6843829.html
    手机设置HTTP代理后无法上网：iphone-->通用-->关于本机-->证书信任设置-->针对根证书启用完全信任
    """

    # 请求地址
    url = "http://hd.konglongcheng.com.cn/HD2018/EXVote/EXVoteHelper.ashx?action=vote&Id=155"
    # 循环投票
    for i in range(1, 100):
        # 请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN",
            "Referer": "http://hd.konglongcheng.com.cn/HD2018/EXVote/index.aspx?txt=155",
            # 修改Cookie值伪装成不同用户
            "Cookie": "comm_hd_cookie=oZCrNjtRiwIwiYmhQ4evBHB7S3zQ" + str(i),
        }
        # 发送get请求
        response = requests.get(url, headers=headers)
        # 查看响应数据
        print(response.text)


def like():
    """
    需求：给微信公众号评论点赞(暂未搞定)
    分析：手机fiddler抓包获取url、User-Agent、Cookie信息
    报错：No connection adapters were found for '%s'" % url --> 是因为url被二次编码了,注意那些带有%的字符
    常用url编码表
    url        编码结果
    空格        %20
    !          %21
    "          %22
    #          %23
    $          %24
    %          %25
    &          %26
    '          %27
    (          %28
    )          %29
    *          %2A
    +          %2B
    ,          %2C
    -          %2D
    .          %2E
    /          %2F
    :          %3A
    ;          %3B
    <          %3C
    =          %3D
    >          %3E
    ?          %3F
    ...
    """

    # """
    # POST https://mp.weixin.qq.com/mp/appmsg_comment?action=likecomment&uin=777&key=777&pass_ticket=f9Hl7tdmFGVJ9Nxlc3%25252FOHoutuqgVYcu2s5OXd7G27WE28bPEwlEpO1RJ4%25252FBaGnet&wxtoken=777&devicetype=iOS12.1.2&clientversion=17000125&appmsg_token=992_3m14iG3Hf%252FcNJmeoT3ccxbw1b5eGv4jxxkMUc-8QGmCWVJ81GhIvXuc6sFVTimJEdOntKLKQaofLFF3S&x5=0&f=json HTTP/1.1
    # Host: mp.weixin.qq.com
    # Accept: */*
    # X-Requested-With: XMLHttpRequest
    # Accept-Language: zh-cn
    # Accept-Encoding: br, gzip, deflate
    # Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    # Origin: https://mp.weixin.qq.com
    # User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16C101 MicroMessenger/7.0.1(0x17000120) NetType/WIFI Language/zh_CN
    # Connection: keep-alive
    # Referer: https://mp.weixin.qq.com/s?__biz=MzUyMjE2MTE0Mw==&mid=2247487327&idx=1&sn=6df996995fc8dbd0d64109dffae57f22&chksm=f9d151c7cea6d8d1a3dc72f14de365db2baf0a83fdd167839517c6f3f3c276332f7140af045b&scene=0&xtrack=1&sessionid=1547794208&subscene=92&clicktime=1547794230&ascene=7&devicetype=iOS12.1.2&version=17000125&nettype=WIFI&abtest_cookie=BQABAAoACwASABMAFAAGACWXHgBXmR4Am5keAJ2ZHgC3mR4A1JkeAAAA&lang=zh_CN&fontScale=100&pass_ticket=f9Hl7tdmFGVJ9Nxlc3%2FOHoutuqgVYcu2s5OXd7G27WE28bPEwlEpO1RJ4%2FBaGnet&wx_header=1
    # Content-Length: 139
    # Cookie: devicetype=iOS12.1.2; lang=zh_CN; pass_ticket=f9Hl7tdmFGVJ9Nxlc3/OHoutuqgVYcu2s5OXd7G27WE28bPEwlEpO1RJ4/BaGnet; rewardsn=; version=17000125; wap_sid2=CLbLm/YDElw5RVNKdmxKZUtqQUhfLXBSSDI0V3R5WC1lN3VvR0FJTkhHa2J6eXRvUGlVOGx5NmNOUEE3NU1TVzkyYXczZVoyQTJDLUV6Q01XSk4zWUNoRUtoaXdrZUFEQUFBfjC37oXiBTgNQAE=; wxtokenkey=777; wxuin=1053222326; pgv_pvid=5661142221; ts_uid=3005708013; _scan_has_moon=1; pgv_pvid_new=085e9858ed6d664b05f8f0fce@wx.tenpay.com_6e8a5dc79c
    #
    # like=1&__biz=MzUyMjE2MTE0Mw%3D%3D&appmsgid=2247487327&comment_id=627588963393601536&content_id=4523555445587050497&item_show_type=0&scene=0
    # """

    # """
    # POST https://mp.weixin.qq.com/mp/appmsg_comment?action=likecomment&uin=777&key=777&pass_ticket=BwTE1aSRvJu%25252FRuU%25252F556rhoFNxuJSCJaDznZqudltWvv3%25252BIE07u6A5GzrLPqlUraa&wxtoken=777&devicetype=iOS12.1.2&clientversion=17000227&appmsg_token=992_OibQx%252BNehjXqXOVJbMfaRSILhUjUXkMdl_f4v1ggyMteZMnDLud29BlUhkYIaOBuczVf13DCYZOmEygP&x5=0&f=json HTTP/1.1
    # Host: mp.weixin.qq.com
    # Accept: */*
    # X-Requested-With: XMLHttpRequest
    # Accept-Language: zh-cn
    # Accept-Encoding: br, gzip, deflate
    # Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    # Origin: https://mp.weixin.qq.com
    # User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16C101 MicroMessenger/7.0.2(0x17000222) NetType/WIFI Language/zh_CN
    # Connection: keep-alive
    # Referer: https://mp.weixin.qq.com/s?fontRatio=1&__biz=MzUyMjE2MTE0Mw==&mid=2247487327&idx=1&sn=6df996995fc8dbd0d64109dffae57f22&scene=94&subscene=315&passparam=searchid%3D13437444122640939076&ascene=0&devicetype=iOS12.1.2&version=17000227&nettype=WIFI&abtest_cookie=BQABAAoACwASABMAFAAGACOXHgBXmR4Am5keAJ2ZHgC2mR4A0pkeAAAA&lang=zh_CN&fontScale=100&pass_ticket=BwTE1aSRvJu%2FRuU%2F556rhoFNxuJSCJaDznZqudltWvv3%2BIE07u6A5GzrLPqlUraa&wx_header=1
    # Content-Length: 139
    # Cookie: wxtokenkey=777; devicetype=iOS12.1.2; lang=zh_CN; pass_ticket=BwTE1aSRvJu/RuU/556rhoFNxuJSCJaDznZqudltWvv3+IE07u6A5GzrLPqlUraa; rewardsn=; version=17000227; wap_sid2=CLfTk/IEElxPa1l6SjRiLXpqYlhWRFVMUVVCUE9heWFKUUtqQmNWNkwtbXgzcVZ2OEVRQ3lrUy05dkV0Ym1SVlFJYXNUUVg4U052R254Z3lMTHBwVTJMdkFabTNGT0FEQUFBfjDol4biBTgNQAE=; wxuin=1313139127; pgv_pvid=9139259760; tvfe_boss_uuid=fe8b18d4d262a66a; sd_cookie_crttime=1527161699327; sd_userid=52701527161699327
    #
    # like=1&__biz=MzUyMjE2MTE0Mw%3D%3D&appmsgid=2247487327&comment_id=627588963393601536&content_id=4523555445587050497&item_show_type=0&scene=0
    # """

    # TODO
    # url = "https://mp.weixin.qq.com/mp/appmsg_comment?action=likecomment&uin=777&key=777&pass_ticket=f9Hl7tdmFGVJ9Nxlc3%25252FOHoutuqgVYcu2s5OXd7G27WE28bPEwlEpO1RJ4%25252FBaGnet&wxtoken=777&devicetype=iOS12.1.2&clientversion=17000125&appmsg_token=992_3m14iG3Hf%252FcNJmeoT3ccxbw1b5eGv4jxxkMUc-8QGmCWVJ81GhIvXuc6sFVTimJEdOntKLKQaofLFF3S&x5=0&f=json"
    url = "https://mp.weixin.qq.com/mp/appmsg_comment?action=likecomment&appmsg_token=992_3m14iG3Hf/cNJmeoT3ccxbw1b5eGv4jxxkMUc-8QGmCWVJ81GhIvXuc6sFVTimJEdOntKLKQaofLFF3S"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16C101 MicroMessenger/7.0.1(0x17000120) NetType/WIFI Language/zh_CN",
        "Cookie": "wap_sid2=CLbLm/YDElw5RVNKdmxKZUtqQUhfLXBSSDI0V3R5WC1lN3VvR0FJTkhHa2J6eXRvUGlVOGx5NmNOUEE3NU1TVzkyYXczZVoyQTJDLUV6Q01XSk4zWUNoRUtoaXdrZUFEQUFBfjC37oXiBTgNQAE=;"
    }
    data = {
        "like": 1,
        "comment_id": 627588963393601536,  # 留言id
        "content_id": 4523555445587050497,  # 留言内容id
    }
    response = requests.post(url=url, data=data, headers=headers)
    print(response.text)


if __name__ == '__main__':
    # vote()
    like()
