import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from prettytable import PrettyTable

from dolphin_monitor import config


def mail(subject, content):
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
    mail(aaa, bbb)