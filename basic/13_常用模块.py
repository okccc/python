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
    sha1.update("123456".encode())
    # 返回160bit=20byte=40位长度的十六进制字符串
    print(sha1.hexdigest())  # 7c4a8d09ca3762af61e59520943dc26494f8941b


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
    """
    python日志处理(logging模块):
    http://www.cnblogs.com/yyds/p/6901864.html
    http://yshblog.com/blog/125

    两种日志记录方式:
    1、使用logging提供的模块级别的函数
    logging.basicConfig(**kwargs)

    2、使用logging日志系统的四大组件
    日志器(Logger): 提供了应用程序可一直使用的接口
    处理器(Handler): 将logger创建的日志记录发送到合适的目的输出
    过滤器(Filter): 提供了更细粒度的控制工具来决定输出哪条日志记录，丢弃哪条日志记录
    格式器(Formatter): 决定日志记录的最终输出格式
    """

    import logging.handlers

    # 方式一：使用logging函数
    # 1.输出在控制台
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S %p"
    )

    # 2.输出到文件
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S %p",
        filename="./log/error.log",
        filemode="a"
    )

    # 方式二：使用logging四大组件
    # 1.创建logger对象
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # 2.创建一个handler用于输出日志到控制台
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    # 3.创建一个handler用于写入日志到文件
    fh = logging.FileHandler(filename='./err.log', mode='a', encoding='utf8')
    fh.setLevel(logging.ERROR)
    # 4.定义handler输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[:%(lineno)d] - %(levelname)s - %(message)s")
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 5.将handler添加到logger
    logger.addHandler(sh)
    logger.addHandler(fh)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')


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
    hashlib01()

