# coding=utf-8
"""
文件读写：
open()：默认r只读,w只写(有内容就覆盖),a追加,r+可读可写;操作图片、视频等二进制文件：rb,wb,ab
read(size)：不写size就一次读取所有行
readline()：每次读取一行,返回str,执行完指针会移到下一行,包括 "\n" 字符
readlines()：一次读取所有行,返回list,每行都是一个元素; f.readlines()[1:]可以通过切片指定读取哪些行
tell()：获取当前文件位置
seek(offset, from)：调整当前文件位置

文件操作:
os.rename()：重命名
os.remove()：刪除文件
os.rmdir()：删除文件夹
os.mkdir()：创建文件夹
os.getcwd()：获取当前目录
os.path.join(os.getcwd(), file)：拼接路径
os.listdir()：遍历指定目录下所有文件(夹)
os.path.isfile()：判断是否是文件
os.path.isdir()：判断是否是文件夹
os.path.getsize()：获取文件大小,求文件夹大小的话需要递归遍历所有文件
os.path.splitext()[1]：获取文件后缀名
os.path.abspath(__file__)：获取当前文件绝对路径
os.path.dirname(__file__)：获取当前文件所在目录
os.path.dirname(os.path.dirname(__file__))：获取当前文件所在目录的上级目录
"""

from moviepy.editor import *  # 合成视频的模块
import os
import re


def recursive(path):
    """递归操作"""
    files = os.listdir(path)
    for file in files:
        if os.path.isfile(path + file):
            if file.endswith(".mp4"):
                file_new = file.replace("内核解析_", "")
                os.rename(path + file, path + file_new)
        else:
            recursive(path + file + "/")


def video_editor():
    """视频剪辑常用功能"""
    target_dir = "/Users/okc/Documents/tmp/"
    filename = target_dir + "d4a6c458673a58e5ba203dbbd452c1f0.mov"
    # 载入视频文件
    video = VideoFileClip(filename)
    # 获取视频信息
    print("分辨率：%s, 时长：%s 秒, 大小：%.2f M" % (video.size, video.duration, os.path.getsize(filename)/1024/1024))
    # 1.截取指定时长片段
    video.subclip(t_start='00:09:23', t_end=video.duration).write_videofile(target_dir + "01.mp4")
    # 2.设置视频倍速播放
    video.speedx(2).write_videofile(target_dir + "02.mp4")
    # 3.截取视频封面
    video.save_frame(target_dir + '01.jpg', t=0)  # t可以指定开头第几秒

    # 4.合并视频小文件
    videos = []
    # for top, dirs, files in os.walk(target_dir):
    files = os.listdir(target_dir)
    for file in files:
        # if os.path.splitext(file)[1] == ".flv":
        # 拼接文件完整路径
        file_path = os.path.join(target_dir, file)
        # 载入待合并的视频文件
        video = VideoFileClip(file_path)
        # 可以剪辑指定时长的视频文件
        video.subclip(t_start=0, t_end=video.duration - 1)
        # 添加到列表
        videos.append(video)
    # 拼接视频
    res = concatenate_videoclips(videos)
    # 生成目标视频文件
    res.to_videofile(target_dir + "a.mp4", fps=24, remove_temp=True)


def test01():
    """往文件的每一行末尾添加两个空格"""
    with open("C://Users/admin/Desktop/projects/hive/hqls/stats.sql", encoding="utf8") as f1:
        with open("C://Users/admin/Desktop/projects/hive/hqls/stats1.sql", "w", encoding="utf8")as f2:
            for line in f1.readlines():
                # split()可去除空白行
                if line.split():
                    # 由于读完每一行会自动换行,所以索引取到-1
                    line_new = line[:-1] + ";" + "\n"
                    f2.write(line_new)


def test02():
    """去除换行符,将多行内容放到同一行"""
    with open("D://PycharmProjects/python/analysis/csv/city.txt", encoding="utf8") as f1:
        with open("D://PycharmProjects/python/analysis/csv/city1.txt", "w", encoding="utf8") as f2:
            for line in f1.readlines():
                f2.write(line[:-1])


def test03():
    """删除符合条件的行"""
    with open("D://PycharmProjects/python/analysis/05_pyecharts可视化.py", encoding="utf8") as f1:
        with open("D://PycharmProjects/python/analysis/05_pyecharts可视化1.py", "w", encoding="utf8") as f2:
            for line in f1.readlines():
                if line.startswith("In") or line.startswith("Out") or re.match("\\d+", line):
                    continue
                f2.write(line)


if __name__ == "__main__":
    # recursive("/Users/okc/Downloads/资料/")
    video_editor()
