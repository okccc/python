# coding=utf-8
"""
文件读写: 一个函数(open),三个方法(read、write、close)
open(): 默认r只读,w只写(有内容就覆盖),a追加,r+可读可写;操作图片、视频等二进制文件: rb,wb,ab
read(size): 不写size就一次读取所有行,返回str,执行完指针会移动到文件末尾
readline(): 每次读取一行,返回str,执行完指针会移到下一行,包括 "\n" 字符
readlines(): 一次读取所有行,返回list,每行都是一个元素; f.readlines()[1:]可以通过切片指定读取哪些行
所以：read()和readline()只能读取文本文件,读取二进制文件得用readlines()
注意：read()和readlines()会把文件所有内容读取到内存，数据量大的话慎用！
tell(): 获取当前文件位置
seek(offset, from): 调整当前文件位置
    offset: 偏移量(注意：utf-8格式中文占3个字节，gbk格式中文占2个字节)
    from: 方向 0表示文件开头 1表示当前位置 2表示文件结尾(python3目前只能写0！)

文件操作:
os.rename(path1, path2): 重命名
os.remove(): 刪除文件
os.rmdir(): 删除文件夹
os.mkdir(): 创建文件夹
os.getcwd(): 获取当前目录
os.listdir(): 遍历指定目录下所有文件(夹),返回list列表
os.path.isfile(): 判断是否是文件
os.path.isdir(): 判断是否是文件夹
os.path.getsize(filename): 获取文件大小,求文件夹大小的话需要递归遍历所有文件
os.path.abspath(__file__): 获取当前文件绝对路径
os.path.dirname(__file__): 获取当前文件所在目录
os.path.dirname(os.path.dirname(__file__)): 获取当前文件所在目录的上级目录
os.path.join(os.getcwd(), "images"): 拼接路径
"""

import os
import re

def recursive(path, suffix):
    # 递归操作
    files = os.listdir(path)
    for file in files:
        if os.path.isfile(path + file):
            if file.endswith(suffix):
                file_new = file.replace(suffix, ".png")
                os.rename(path + file, path + file_new)
        else:
            recursive(path + file + "/", suffix)

def test01():
    # 往文件的每一行末尾添加两个空格
    with open("C://Users/admin/Desktop/xixi", encoding="utf8") as f1:
        with open("C://Users/admin/Desktop/haha", "w", encoding="utf8")as f2:
            for line in f1.readlines():
                # split()可去除空白行
                if line.split():
                    # 由于读完每一行会自动换行,所以索引取到-1
                    line_new = line[:-1] + "  " + "\n"
                    f2.write(line_new)

def test02():
    # TODO
    # 合并小文件: 如果是视频文件合并后会出错,要用moviepy
    dir = "D://test/"
    files = os.listdir(dir)
    with open("D://test/test.mp4", "wb") as f:
        for file in files:
            f.write(open(dir+file, 'rb').read())

def test03():
    # 去除换行符,将多行内容放到一行
    with open("D://PycharmProjects/python/analysis/csv/city.txt", encoding="utf8") as f1:
        with open("D://PycharmProjects/python/analysis/csv/city1.txt", "w", encoding="utf8") as f2:
            for line in f1.readlines():
                f2.write(line[:-1])

def test04():
    # 删除符合条件的行
    with open("D://PycharmProjects/python/analysis/05_pyecharts可视化.py", encoding="utf8") as f1:
        with open("D://PycharmProjects/python/analysis/05_pyecharts可视化1.py", "w", encoding="utf8") as f2:
            for line in f1.readlines():
                if line.startswith("In") or line.startswith("Out") or re.match("\d+", line):
                    continue
                f2.write(line)


if __name__ == "__main__":
    # recursive("D://PycharmProjects/python/", ".jpeg")
    test01()
    # test02()
    # test03()
    # test04()
