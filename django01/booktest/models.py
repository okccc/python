"""
设计和数据库表对应的模型类

错误：将数据库从sqlite3切换到mysql时：django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'
原因：python2使用mysqldb连接mysql,python3使用pymysql连接mysql
解决：pip install pymysql,并在project的__init__.py文件添加
     import pymysql
     pymysql.install_as_MySQLdb()
"""
from django.db import models

class BookInfo(models.Model):
    """图书模型类"""
    btitle = models.CharField(max_length=20)  # 名称
    bpub_date = models.DateField()  # 出版日期

    def __str__(self):
        # 默认返回object对象,需转化为字符串
        return self.btitle


class HeroInfo(models.Model):
    """英雄模型类"""
    hname = models.CharField(max_length=10)  # 名称
    hgender = models.BooleanField(default=False)  # 性别
    hcomment  = models.CharField(max_length=50)  # 备注
    # 在一对多关系的多方添加外键
    hbook = models.ForeignKey('BookInfo')

    def __str__(self):
        return self.hname
