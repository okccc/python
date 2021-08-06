# coding=utf-8
import time
import pymysql
from prettytable import PrettyTable
from jinja2 import Environment, FileSystemLoader

from dolphin_monitor import config
from dolphin_monitor import alarm

# 获取数据库连接
conn = pymysql.connect(**config.mysql)
# 创建游标
cur = conn.cursor()

# 获取当前日期和小时
current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
current_date = current_time[0: 10]  # 2021-06-08
current_hour = current_time[11: 16]  # 14:39

# 查询整体作业执行情况
with open("01.sql") as f:
    sql01 = "".join(f.readlines())
# 已执行任务,成功任务,运行中任务,失败任务
cnt1, cnt2, cnt3, cnt4 = 0, 0, 0, 0
try:
    # 执行sql
    cur.execute(sql01 % current_date)
    # 获取执行语句的返回结果
    res = cur.fetchall()
    # print(res)  # (('运行中', 11), ('成功', 494))
    for (state, num) in res:  # 注意：这里不能再写cur.fetchall()了,不然相当于执行了两次
        cnt1 += num
        if state == '成功':
            cnt2 += num
        if state == '运行中':
            cnt3 += num
    cnt4 = cnt1 - cnt2 - cnt3
except Exception as e:
    print(e)

# 创建表格
table = PrettyTable(['作业id', '作业名称', '项目名称', '状态', '创建者', '尝试次数'])
# 查询未完成作业详情
with open("02.sql") as f:
    sql02 = "".join(f.readlines())
try:
    # 执行查询获取结果
    cur.execute(sql02 % current_date)
    # 往表格添加行数据
    res = cur.fetchall()
    # print(res)  # ((5, 't1', 'ODS', '成功', 'andy', '1'), (6, 't2', 'DWD', '失败', 'lucy', '1'))
    for (pid, name1, name2, state, owner, times) in res:
        if state == "失败" or state == "停止":
            table.add_row([pid, name1, name2, state, owner, times])
except Exception as e:
    print(e)

# 发送邮件
# 主题
subject = '{0} 调度任务失败数 {1}'.format(current_time, cnt4)
# 加载html模板
loader = FileSystemLoader(searchpath='./templates')
env = Environment(loader=loader)
template = env.get_template('email.html')
# 渲染模板,填充数据
content = template.render(
    monitorAll={
        'allJobs': cnt1,      # 已执行作业数
        'successJobs': cnt2,  # 成功作业数
        'runningJobs': cnt3,  # 运行中作业数
        'failJobs': cnt4,     # 失败作业数
        'successRate': '{:.2%}'.format(cnt2 / cnt1),  # 成功率,保留2位小数
    },
    unsuccessJobs=table.get_html_string()
)

# 白天有任务失败才发送告警邮件,每天早上6:30也会发邮件看看凌晨调度跑咋样了
if cnt3 > 0 or current_hour == '06:30':
    if alarm.sendMail(subject, content):
        print("send mail success!")
    else:
        print("send email fail!")

# 关闭游标和连接
cur.close()
conn.close()