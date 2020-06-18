import requests
from lxml import etree

url = "https://i.meituan.com/poi/1346931863?channel=beauty&ct_poi=247454901722043440443871103288791440370_a1346931863_c3"
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            # "Host": "i.meituan.com",
        }
response = requests.get(url, headers=headers)
html = etree.HTML(response.text)
address_tmp = html.xpath('//div[@class="poi-address"]/text()')
star_tmp = html.xpath('//a[@class="react"]//em[@class="star-text"]/text()')
num_tmp = html.xpath('//span[@class="pull-right"]/text()')
print(address_tmp)
print(star_tmp)
print(num_tmp)
