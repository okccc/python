# import requests, pdfkit
# from bs4 import BeautifulSoup
#
# r = requests.get('https://mp.weixin.qq.com/s/FEt9yawhaaje1M_r4DRQpA')
# soup = BeautifulSoup(r.text, 'html.parser')
#
#
# #%%
# target = soup.findAll('p')
#
# for item in target:
#     for link in item.findAll('a'):
#         href = link.get('href')
#         if href.startswith('http'):
#             # 特殊处理图片，增加src
#             r = requests.get(href)
#             soup = BeautifulSoup(r.text, 'html.parser')
#             imgs = soup.findAll('img')
#             for img in imgs:
#                 if img.get('data-src'):
#                     img['src'] = img['data-src']
#             # 生成文件
#             print(item.text)
#             try:
#                 pdfkit.from_string(
#                         soup.prettify(),
#                         'files/' + item.text.strip().replace(' ','_') + '.pdf'
#                 )
#             except:
#                 pass




def test():
    import requests

    url = "http://szextshort.weixin.qq.com/mmtls/2ec2ec95"
    # url = "https://baike.sogou.com/m/getLemmaParagraph?action=2&lemmaId=6373535&contentId=179389089&isNewLemma=false&isHotLemma=true&hasWeibo=false&startDirId=-9&endDirId=&_=1548146070595"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN",
    }
    data = {}
    response = requests.post(url, data=data, headers=headers)
    print(response.status_code)


if __name__ == '__main__':
    test()