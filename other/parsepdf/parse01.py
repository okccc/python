# coding: utf-8
import pdfplumber
import json
import re
import os
import time
# import logging
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     datefmt="%m/%d/%Y %H:%M:%S %p"
# )


def parse_pdf01(path):

    fields = [
        "id", "name", "card_id", "currency", "account", "begin_time", "end_time", "income_total",
        "income_num", "income_total_capital", "pay_total", "pay_num", "pay_total_capital"
    ]

    value_list = []

    files = os.listdir(path)
    for file in files:

        # 打开pdf文件
        pdf = pdfplumber.open(path + file)

        value = []

        pattern1 = re.compile("([\u4e00-\u9fa5]{2}).*(\d{35,})")
        pattern2 = re.compile("([\u4e00-\u9fa5]{3}).(.+)\(")
        pattern3 = re.compile("([\u4e00-\u9fa5]{4}).(\w{18})")
        pattern4 = re.compile("([\u4e00-\u9fa5]{2}).(.+)/")

        text = pdf.pages[0].extract_text()
        m1 = pattern1.match(text)
        m2 = pattern2.search(text)
        m3 = pattern3.search(text)
        m4 = pattern4.search(text)
        id = m1.group()[4:]   # 编号
        # id = m1.group(2)   # 编号
        name = m2.group(2) if m2 else ''  # 姓名
        card_id = m3.group(2) if m3 else ''  # 证件号码
        currency = m4.group(2) if m4 else ''  # 币种

        table = pdf.pages[0].extract_table()
        account = table[1][2]  # 支付宝账号
        begin_time = table[2][2][2:21]  # 起始时间
        end_time = table[2][2][24:-1]  # 结束时间
        income_total = table[3][2]  # 收入总金额
        income_num = table[3][6]  # 收入总笔数
        income_total_capital = table[4][2]  # 收入总金额大写
        pay_total = table[5][2]  # 支出总金额
        pay_num = table[5][6]  # 支出总笔数
        pay_total_capital = table[6][2]  # 支出总金额大写

        data = {
            "id": id,
            "name": name,
            "card_id": card_id,
            "currency": currency,
            "account": account,
            "begin_time": begin_time,
            "end_time": end_time,
            "income_total": income_total,
            "income_num": income_num,
            "income_total_capital": income_total_capital,
            "pay_total": pay_total,
            "pay_num": pay_num,
            "pay_total_capital": pay_total_capital
        }

        for field in fields:
            value.append(data.get(field))
        value.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        value_list.append(value)

    return value_list


if __name__ == "__main__":
    res = parse_pdf01("./pdf/")
    print(res)
    json.dump(res, open("./value/01.txt", "w", encoding="utf-8"), ensure_ascii=False)