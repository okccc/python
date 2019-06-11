from django.conf.urls import url
from . import views

# 配置url路由
urlpatterns = [
    url('^$', views.index),
    url('^index/$', views.index),

    # (1)位置参数：视图参数名随便指定
    url('^index/(\d+)/$', views.detail01),
    url('^index/(\d+)/(\d+)/$', views.detail02),
    # (2)关键字参数(?P<组名>)：视图参数名要和正则组名一致
    url('^(?P<num>\d+)/$', views.detail01),

    url('^add/$', views.add),
    url('^delete(\d+)/$', views.delete),
    url('^areas/$', views.areas),  # 地区信息

    url('^login/$', views.login),
    url('^login_check', views.login_check),
    url('^login_ajax$', views.login_ajax),
    url('^login_ajax_check', views.login_ajax_check),
    url('^cookie01', views.cookie01),
    url('^session01', views.session01),
    url('^template01', views.template01),
    url('^inherit', views.inherit),
    url('^escape', views.escape),
]


