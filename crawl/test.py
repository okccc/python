import requests, pdfkit
from bs4 import BeautifulSoup

r = requests.get('https://mp.weixin.qq.com/s/FEt9yawhaaje1M_r4DRQpA')
soup = BeautifulSoup(r.text, 'html.parser')


#%%
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