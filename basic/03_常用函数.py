# coding=utf-8

# input(): 键盘录入只能输入字符串,数字类型要用int,float等函数转换
price = float(input("请输入单价:"))
weight = int(input("请输入重量:"))
money = price * weight
print(money)

# eval(): 可以将输入的字符串当成有效表达式(取字符串里的内容)并返回计算结果
result = eval(input("输入算术题:"))
print(result)

# id(): 可以查看变量在内存中的地址值
num = 10
addr = id(num)
print("%d" % addr)  # 1699763280 (%d以十进制输出结果)
print("%x" % addr)  # 65505450 (%x以十六进制输出结果)

"""
print(): 默认换行,在结尾添加end=""可以不换行接着输出
%表示格式化输出符: 当print函数输出的内容包含多种不同类型的变量,就要对变量进行格式化
%s:字符串  %d:整数  %f:小数  %%:输出%
"""

# 格式化输出字符串
name = "小花"
print("大家好我叫 %s" % name)

# 格式化输出整数(06控制长度,不满6位以0补全)
num = 19
print("我的学号是 %06d" % num)

# 格式化输出小数(.2控制长度,小数点后面保留2位)
price = 4.5
weight = 5
money = price * weight
print("苹果单价 %.2f 元/斤,重量 %d 斤,总价 %.2f 元" % (price, weight, money))  # 多个变量放()里用, 隔开

# 格式化输出百分比
scale = 0.25
print("数据比例是 %.2f%%" % (scale * 100))


