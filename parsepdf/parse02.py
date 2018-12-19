# coding: utf-8
"""
61/75行报错：AttributeError: 'str' object has no attribute 'strftime'
注意：mysql表字段不能用到python里的关键字，比如time既是字段又是模块，会冲突
"""

import pdfplumber
import re
import json
import os
import time


def parse_pdf02(path):

    # mysql表字段
    fields = [
        "id", "flow_id", "create_time", "remark", "income", "pay", "account_surplus", "fund_channel"
    ]

    # 存放多条value的列表
    value_list = []

    files = os.listdir(path)
    for file in files:

        # 打开pdf文件
        pdf = pdfplumber.open(path + file)

        text = pdf.pages[0].extract_text()
        pattern = re.compile("([\u4e00-\u9fa5]{2}).*(\d{35,})")
        m = pattern.search(text)
        # 支付宝账号
        id = m.group()[4:]

        # 遍历pdf文件的每一页
        for page in pdf.pages:
            # 首页
            if page == pdf.pages[0]:
                table = page.extract_table()
                for each in table[9:]:
                    get_field(id, each, fields, value_list)
            # 其他页
            else:
                try:
                    table = page.extract_table()
                    for each in table:
                        get_field(id, each, fields, value_list)
                except Exception as e:
                    print(e)
                    continue
    return value_list


def get_field(id, each, fields, value_list):
    # 单条value值
    value = []

    flow_id = each[0]  # 流水号
    create_time = each[1]  # 生成时间
    remark = each[2]  # 名称/备注
    income = each[3] if each[3] != '' else 0  # 收入
    pay = each[4] if each[4] != '' else 0  # 支出
    account_surplus = each[5] if each[5] != '' else 0  # 账户余额
    fund_channel = "".join(each[6].split())  # 资金渠道
    data = {
        "id": id,
        "flow_id": flow_id,
        # "time": time,
        "create_time": create_time,
        "remark": remark,
        "income": income,
        "pay": pay,
        "account_surplus": account_surplus,
        "fund_channel": fund_channel
    }

    # 遍历mysql表字段
    for field in fields:
        # 往value添加字段值
        value.append(data.get(field))
    value.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # 将单条value添加到value集合
    value_list.append(value)


if __name__ == "__main__":
        res = parse_pdf02("./pdf/")
        print(res)
        # 将结果保存到中间件
        json.dump(res, open("./value/02.txt", "w", encoding="utf-8"), ensure_ascii=False)
