# coding=utf-8
"""
argparse是Python标准库中推荐使用的命令行解析模块,可以在执行Python xx.py时添加各种命令行参数
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