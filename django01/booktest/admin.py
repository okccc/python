"""
注册模型类
Django提供了admin.ModelAdmin类,通过定义其子类来自定义模型在admin界面的显示方式

"""
from django.contrib import admin
from .models import BookInfo, HeroInfo

# 自定义模型管理类
class BookInfoAdmin(admin.ModelAdmin):
    """图书模型管理类"""

    # list_display：显示字段(可调整字段顺序且字段可排序)
    list_display = ['id', 'btitle', 'bpub_date']


class HeroInfoAdmin(admin.ModelAdmin):
    """英雄模型管理类"""

    list_display = ['id', 'hname', 'hcomment', 'hbook']


# 注册模型到admin
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)