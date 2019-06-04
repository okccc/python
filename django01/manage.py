#!/usr/bin/env python
"""
manage.py是一个命令行工具,可以使用多种方式和Django项目做交互

创建项目：django-admin startproject django01
创建应用：python manage.py startapp booktest
    在项目里注册应用：settings --> INSTALLED_APPS --> 'booktest'
    添加允许访问的主机：settings --> ALLOWED_HOSTS --> '192.168.152.11'
启动服务器：python manage.py runserver ip:port
models
    1.创建模型类：models.py --> BookInfo(models.Model)
    2.修改数据库配置信息：settings --> DATABASES --> mysql
    3.生成迁移文件：python manage.py makemigrations
    4.执行迁移：python manage.py migrate
    5.测试数据：python manage.py shell
admin
    1.语言和时间本地化：settings --> LANGUAGE_CODE、TIME_ZONE
    2.创建管理员用户：python manage.py createsuperuser
    3.登录admin管理页面：http://192.168.152.11:9999/admin/
    3.注册模型类：admin.py --> admin.site.register()
    4.自定义管理页面：admin.py --> BookInfoAdmin(admin.ModelAdmin)
views
    1.定义视图函数：views.py --> def xxx(request)
    2.配置对应的url路由：booktest/urls.py --> urlpatterns
    3.将app的urls添加到project的主urls：django01/urls.py --> urlpatterns
templates
    1.创建模板文件夹
    2.修改模板配置信息：settings --> TEMPLATES
    3.加载模板文件

booktest
    ── admin.py                           网站后台管理相关
    ── apps.py
    ── __init__.py
    ── migrations
        ── __init__.py
    ── models.py                          和数据库交互
    ── tests.py                           测试代码
    ── views.py                           定义处理(视图)函数
django01
    ── __init__.py                        说明django01是一个python包
    ── settings.py                        项目配置文件
    ── urls.py                            配置url路由
    ── wsgi.py                            web服务器和django交互的入口
manage.py                                  项目管理文件

常见错误：
1、django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'(见models.py)
2、OSError: No translation files found for default language zh-CN
原因：新版本的django不支持zh-CN, 查看/home/.virtualenvs/django/lib/python3.6/site-packages/django/conf/locale目录下没有zh-CN
解决：修改settings.py --> LANGUAGE_CODE = 'zh-Hans'
3、DisallowedHost: Invalid HTTP_HOST header: '192.168.19.11:7777'. You may need to add '192.168.19.11' to ALLOWED_HOSTS.
解决：修改settings.py --> ALLOWED_HOSTS = ['*']
4、redis.exceptions.ConnectionError: Error -2 connecting to localhost:6379. Name or service not known.
解决：修改/etc/hosts --> 添加一行 127.0.0.1  localhost
"""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django01.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
