# coding=utf-8
"""
python日志处理(logging模块):
http://www.cnblogs.com/yyds/p/6901864.html
http://yshblog.com/blog/125

两种日志记录方式:
1、使用logging提供的模块级别的函数
logging.basicConfig(**kwargs)

2、使用Logging日志系统的四大组件
日志器(Logger): 提供了应用程序可一直使用的接口
处理器(Handler): 将logger创建的日志记录发送到合适的目的输出
过滤器(Filter): 提供了更细粒度的控制工具来决定输出哪条日志记录，丢弃哪条日志记录
格式器(Formatter): 决定日志记录的最终输出格式
"""

import logging.handlers
import datetime

"""
方式一：使用logging函数
"""
# 输出在控制台
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     datefmt="%m/%d/%Y %H:%M:%S %p"
# )

# 输出到文件
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     datefmt="%m/%d/%Y %H:%M:%S %p",
#     filename="./log/error.log",
#     filemode="a"
# )

"""
方式二：使用Logger四大组件
"""
def mylogger():

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    rf_handler = logging.handlers.TimedRotatingFileHandler('./log/all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    f_handler = logging.FileHandler('./log/err.log')
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')


if __name__ == "__main__":
    mylogger()