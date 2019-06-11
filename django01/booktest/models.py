"""
设计和数据库表对应的模型类

错误：将数据库从sqlite3切换到mysql时：django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'
原因：python2使用mysqldb连接mysql,python3使用pymysql连接mysql
解决：pip install pymysql,并在project的__init__.py文件添加
     import pymysql
     pymysql.install_as_MySQLdb()
"""
from django.db import models

class BookInfoManager(models.Manager):
    """模型管理器类"""
    def all(self):
        # 作用一：修改默认查询集
        return super().all().filter(isDelete=False)

    def create(self, title, pub_date):
        # 作用二：封装crud功能
        book = self.model()  # self.model自动获取当前管理器所属的模型类,这样即使模型类改名字也没关系
        book.title = title
        book.pub_date = pub_date
        book.save()
        return book


class BookInfo(models.Model):
    """图书模型类"""
    title = models.CharField(max_length=20, unique=True, db_index=True, db_column='title')
    pub_date = models.DateField(null=False)
    reading = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        # 默认返回object对象,需转化为字符串
        return self.title

    # django默认管理器是objects,可以使用自定义管理器
    objects = BookInfoManager()

    # 定义元选项：模型类在数据库中对应的表名默认是app_model,可以在Meta()类定义表的元数据信息
    class Meta():
        # 修改默认表名
        db_table = "bookinfo"

class HeroInfo(models.Model):
    """英雄模型类"""
    name = models.CharField(max_length=10)
    gender = models.BooleanField(default=False)
    introduce = models.CharField(max_length=50, null=True, blank=True)  # blank是在后台管理时控制是否可以填写空白
    isDelete = models.BooleanField(default=False)
    # 在一对多关系(重点)的多方添加外键
    book = models.ForeignKey('BookInfo')
    # 如果是一对一或者多对多的关系,外键定义在任何一方都可以
    # book = models.OneToOneField('BookInfo')
    # book = models.ManyToManyField('BookInfo')

    def __str__(self):
        return self.name

    class Meta():
        db_table = "heroinfo"

    # 通过模型类实现关联查询时,要查哪个表数据就用哪个模型类查


class AreaInfo(models.Model):
    """地区模型类"""
    title = models.CharField(max_length=20)  # 名称
    # 自关联：地区、分类等表结构很相似且每个表的数据量很少,可以设计成一张表,内部关系字段指向本表主键 --> 是特殊的一对多模型
    # 关系属性使用self指向本类,由于一级数据没有父级,所以null和blank要允许为空
    parent = models.ForeignKey('self', null=True, blank=True)  # 上级关系

    def __str__(self):
        return self.title

    class Meta():
        db_table = "areainfo"