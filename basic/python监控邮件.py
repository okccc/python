# coding=utf-8
"""
收发邮件库：smtplib、poplib、imaplib
发送邮件使用SMTP协议(Simple Mail Transfer Protocol)
接收邮件使用POP3协议(Post Office Protocol)和IMAP(Internet Mail Access Protocol)
POP和IMAP的区别：
POP在客户端邮箱中所做的操作不会反馈到邮箱服务器,比如删除一封邮件,邮箱服务器并不会删除
IMAP则会反馈到邮箱服务器会做相应的操作
参考文档：https://www.cnblogs.com/fnng/p/7967213.html
"""

import yagmail
import pymysql
import os
from datetime import datetime, timedelta


# 发邮件
def send_mail(table_name):
    # 连接邮箱服务器
    yag = yagmail.SMTP(host="smtp.exmail.qq.com", user="chenqian@meihaofenqi.com", password="123456")
    # 收件人(多个收件人可用list表示)
    to = "chenqian@meihaofenqi.com"
    # 抄送人
    cc = "1573976179@qq.com"
    # 主题
    subject = "mysql表结构监控"
    # 正文
    contents = "%s表新增字段!" % table_name
    # 附件
    files = "./高铁线路图.pdf"
    # 发送
    yag.send(to=to, subject=subject, contents=contents, attachments=files, cc=cc)


def monitor_mysql():
    # 数据库配置信息
    config = {
        "host": "10.9.169.3",
        "port": 3306,
        "user": "xxx",
        "password": "xxx",
        "db": "duckchatdb",
        "charset": "utf8",
        "cursorclass": pymysql.cursors.DictCursor  # 以dict格式返回数据
    }
    # 连接数据库
    conn = pymysql.connect(**config)
    # 创建游标
    cur = conn.cursor()
    try:
        # 监控指定库下的表
        sql = "select count(*) as num from information_schema.columns where table_schema='duckchatdb' and table_name=%s"
        # 判断字段数
        cur.execute(sql, "debit_order")
        if cur.fetchall()[0]['num'] != 129:
            send_mail("debit_order")
        cur.execute(sql, "debit_order_ext")
        if cur.fetchall()[0]['num'] != 72:
            send_mail("debit_order_ext")
        cur.execute(sql, "debit_detail")
        if cur.fetchall()[0]['num'] != 34:
            send_mail("debit_detail")
        cur.execute(sql, "shop")
        if cur.fetchall()[0]['num'] != 54:
            send_mail("shop")
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


def monitor_process():
    # 先判断该进程是否卡死
    process = '/home/mhfq.lock'
    os.system(command="ps -aux | grep mhfq_sentiment.py | grep -v grep | awk '{print $2}' > %s" % process)
    if os.path.getsize(process) > 1:
        with open(process) as f:
            lines = f.readlines()
            for line in lines:
                # 杀掉卡死进程
                os.system(command='kill -9 %d' % int(line[:-1]))
        # 重启进程
        os.system(command='/data/anaconda/bin/python /data/app/reports/mhfq_sentiment.py')


def monitor_log():
    # 获取昨天日期
    yesterday = (datetime.today()+timedelta(-1)).strftime('%Y%m%d')
    # 监控指定目录下的log文件
    res = os.popen("cd /data/logs/hql/%s && grep 'FAILED' *.log | awk -F: '{print $1}' | uniq" % yesterday)
    if res:
        for i in res:
            send_mail(i[:-1])


if __name__ == "__main__":
    monitor_mysql()