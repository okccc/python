# coding=utf-8

import os

# dir = "C://Users/chenq/PycharmProjects/Python/"
# def digui(path):
#     file_list = os.listdir(path)
#     for file in file_list:
#         if not file.startswith("."):
#             if os.path.isfile(path+file):
#                 if file.endswith(".py"):
#                     print(file)
#                     with open(path+file,"r+",encoding="utf-8") as f:
#
#                         if f.readline().find("coding") == -1:
#                             f.seek(0,0)
#                             text = f.read()
#                             f.seek(0,0)
#                             f.write("# coding=utf-8\n"+text)
#             else:
#                 digui(path+file+"/")
# digui(dir)

l = ['aaa','bbb']
print(l[0])
print(len(l))