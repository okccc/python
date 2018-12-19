# coding=utf-8
import openpyxl

def test01():
    # 打开xlsx文件
    wb = openpyxl.load_workbook("C://Users/chenq/Desktop/中间表-申请字段.xlsx")
    # 查看sheet页
    print(wb.sheetnames)  # ['Sheet2', 'Sheet1']
    # 选取sheet页
    sheet = wb["Sheet1"]
    # print(sheet)  # <Worksheet "Sheet1">
    # print(type(sheet))  # <class 'openpyxl.worksheet.worksheet.Worksheet'>
    # 读取指定内容
    for field in sheet["2"]:
        print(field.value)


if __name__ == "__main__":
    test01()