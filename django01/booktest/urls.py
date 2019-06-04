from django.conf.urls import url
from . import views

# 配置url路由
urlpatterns = [
    # 通过位置参数传递给视图
    url('^$', views.index),
    # 通过关键字参数(?P<关键字>)传递给视图
    url('^(?P<num>\d+)/$', views.detail01),
    url('^(?P<num1>\d+)/(?P<num2>\d+)/$', views.detail02),
]