# coding=utf-8
import itchat
import pandas as pd
from pyecharts import Map


itchat.login()
friends = itchat.get_friends(update=True)
print(type(friends))  # <class 'itchat.storage.templates.ContactList'>
df = pd.DataFrame(friends)
print(type(df))  # <class 'pandas.core.frame.DataFrame'>
province = df.Province
print(type(province))  # <class 'pandas.core.series.Series'>
print(province)
count = province.value_counts()
print(type(count))  # <class 'pandas.core.series.Series'>
count = count[count.index != '']
print(count)
address = list(count.index)
num = list(count.values)
map = Map(title="微信好友分布", width=1000, height=500)
map.add("", address, num, maptype="china", is_visualmap=True, visual_text_color='#000')
map.render("D://PycharmProjects/python/analysis/aaa.html")
