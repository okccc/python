# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from prettytable import PrettyTable
import requests
import datetime

from dolphin_monitor import config


# 邮件告警
def sendMail(subject, content):
    # 获取发件人信息
    host = config.smtpserver['host']
    sender = config.smtpserver['user']
    password = config.smtpserver['password']
    # 获取收件人信息
    receiver = ", ".join(config.receivers['dw'])

    # 创建MIMEText,传入文本内容、文本格式、字符编码
    msg = MIMEText(content, 'html', 'utf-8')
    # 设置邮件的主题、发件人、收件人
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        # 连接邮箱服务器
        smtp = smtplib.SMTP(host)
        # 可以查看和smtp服务器的详细交互信息
        # smtp.set_debuglevel(1)
        # 登录邮箱
        smtp.login(sender, password)
        # 发送邮件
        smtp.sendmail(sender, receiver, msg.as_string())
        # 退出服务器
        smtp.quit()
        return True
    except Exception as e:
        print(e)
        return False


# 短信告警
def sendMsg():
    pass


# 电话告警
def sendPhone():
    # 请求地址
    url = "https://alarm.jiliguala.com/api/Alarm/sendByPhone?templateName=tt_call&type=txdh&phone={}"
    # 请求头
    headers = {
        "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Content-Type": "application/json;charset=UTF-8"
    }
    # 请求数据,具体数字是某个sql查询结果
    data = {"": ""}
    # 判断今天是星期几(0表示星期一)
    weekday = datetime.datetime.now().weekday() + 1
    # 值班人员名单
    phones = {
        1: "15123065863",  # 星期一
        2: "18851401238",  # 星期二
        3: "13818427154",  # 星期三
        4: "18934550193",  # 星期四
        5: "15601851503",  # 星期五
        6: "17821030027",  # 星期六
        7: "13052295568"   # 星期日
    }
    # 获取今天值班人员电话
    phone = phones.get(weekday)
    # 发送post请求
    response = requests.post(url.format(phone), headers=headers, data=data)
    print(response.text)


if __name__ == '__main__':
    # 邮件主题
    aaa = '调度监控告警'
    # 加载html模板
    loader = FileSystemLoader(searchpath='./templates')
    env = Environment(loader=loader)
    file = env.get_template('email.html')
    table2 = PrettyTable(['作业id', '作业名称', '项目名称', '状态', '创建者', '尝试次数', '下游项目数'])
    table2.add_row((1, 'aa', 'bb', 'success', 'admin', '3', 'no'))
    # 渲染模板,填充参数
    bbb = file.render(
        monitorAll={
            'allJobsCount': 100,  # 已执行作业数
            'successJobs': 20,  # 成功作业数
            'runningJobs': 60,  # 运行中作业数
            'failJobs': 20,  # 失败作业数
            'successRate': '{:.2%}'.format(20 / 100),  # 成功率
        },
        unsuccessJobs=table2.get_html_string(),
    )
    # sendMail(aaa, bbb)

    sendPhone()
