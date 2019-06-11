# coding=utf8
"""
过滤器就是python中的函数,注册后就可以在模板中当作过滤器使用
自定义过滤器：
1.先在app下新建templatetags目录
2.在templatetags目录下新建filters.py
3.在模板html文件中用load标签引入模块
"""
from django.template import Library

# 创建Libraty对象
register = Library()

# 自定义过滤器
@register.filter
def mod(num):
    """判断num是否为偶数"""
    return num % 2 == 0

@register.filter
def mod_val(num, val):
    """判断num是否能被val整除"""
    return num % val == 0