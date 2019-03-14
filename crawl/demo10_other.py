import requests
import pdfkit
from bs4 import BeautifulSoup
import itchat
import pandas as pd
from pyecharts import Map

def test():
    r = requests.get('https://mp.weixin.qq.com/s/FEt9yawhaaje1M_r4DRQpA')
    soup = BeautifulSoup(r.text, 'html.parser')
    target = soup.findAll('p')

    for item in target:
        for link in item.findAll('a'):
            href = link.get('href')
            if href.startswith('http'):
                # 特殊处理图片，增加src
                r = requests.get(href)
                soup = BeautifulSoup(r.text, 'html.parser')
                imgs = soup.findAll('img')
                for img in imgs:
                    if img.get('data-src'):
                        img['src'] = img['data-src']
                # 生成文件
                print(item.text)
                try:
                    pdfkit.from_string(
                            soup.prettify(),
                            'files/' + item.text.strip().replace(' ','_') + '.pdf'
                    )
                except:
                    pass


def weixin_friends():
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
