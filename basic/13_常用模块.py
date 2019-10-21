# coding=utf-8
import hashlib

def hashlib01():
    """
    hashlib: 提供摘要算法(md5、sha1...) --> 将任意长度的数据(明文)以不可逆的方式转换为固定长度的16进制字符串(密文),适用于验证用户登录等
             md5(message-Digest Algorithm 5)消息摘要算法
             sha1(secure hash Algorithm 1)安全哈希算法
    """

    # 创建md5对象
    md5 = hashlib.md5()
    print(md5)  # <md5 HASH object @ 0x0000020D5C1709E0>
    md5.update("hello".encode())
    # 返回128bit=16byte=32位长度的十六进制字符串
    print(md5.hexdigest())  # 5d41402abc4b2a76b9719d911017c592

    # 创建sha1对象
    sha1 = hashlib.sha1()
    print(sha1)  # <sha1 HASH object @ 0x000001E4540F2C60>
    sha1.update("grubby".encode())
    sha1.update("123456".encode())
    # 返回160bit=20byte=40位长度的十六进制字符串
    print(sha1.hexdigest())  # 07270ab4fea0ea853e5f2009e2f4abbbaf5c2ebb


def argparse01():
    """
    argparse：是Python标准库中推荐使用的命令行解析模块,可以在执行Python xx.py时添加各种命令行参数
    """
    import argparse

    # 创建参数解析器
    parser = argparse.ArgumentParser()
    # 添加定位参数(必选参数: 使用时不需要加参数名)
    parser.add_argument("a")
    # 添加可选参数(要传值: 使用时要加参数名 )
    parser.add_argument("-i", "--insert", help="insert data...")
    # 添加可选参数(不需要传值: action=”store_true”可以控制可选参数是否传值)
    parser.add_argument("-p", "--parse", action="store_true", help="parse data...")
    # 解析参数
    args = parser.parse_args()
    # 判断参数并根据不同的参数值执行不同的命令
    if args.insert:
        pass
    if args.parse:
        pass


def logging01():
    import logging
    from logging.handlers import RotatingFileHandler  # 日志记录器

    # 设置日志级别
    logging.basicConfig(level=logging.DEBUG)
    # 创建日志记录器：指明日志保存路径,每个日志文件的最大大小,保存的日志文件个数上限
    log_handler = RotatingFileHandler(".log", maxBytes=1024, backupCount=10, encoding='utf8')
    # 创建日志记录格式：级别 文件:行号 信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 给日志记录器设置日志格式
    log_handler.setFormatter(formatter)
    # 为全局日志工具对象添加日志记录器
    logging.getLogger().addHandler(log_handler)
    # 测试数据
    logging.debug('debug message')
    logging.info('info message')
    logging.warning('warning message')
    logging.error('error message')


def openpyxl01():
    """
    openpyxl：读取excel数据
    """
    import openpyxl

    # 打开xlsx文件
    wb = openpyxl.load_workbook("C://Users/chenqian/Desktop/中间表-申请字段.xlsx")
    # 查看sheet页
    print(wb.sheetnames)  # ['Sheet2', 'Sheet1']
    # 选取sheet页
    sheet = wb["Sheet1"]
    # print(sheet)  # <Worksheet "Sheet1">
    # print(type(sheet))  # <class 'openpyxl.worksheet.worksheet.Worksheet'>
    # 读取指定行数据
    for field in sheet["2"]:
        print(field.value)


if __name__ == '__main__':
    logging01()

