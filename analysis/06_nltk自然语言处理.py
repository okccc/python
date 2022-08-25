# coding=utf-8
"""
NLTK是Python自然语言处理工具包
分类: 根据词性来分(词性标注);名词、形容词、动词等...
分词: 根据语义来分
"""

import nltk  # 调用nltk包管理工具,可以下载语料库和模型等数据;其中Brown语料库和Punkt分词模型必装
# nltk.download()
from nltk.corpus import brown  # 导入布朗大学语料库
import jieba  # 中文分词器
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer  # 需事先安装好wordnet语料库
from nltk.corpus import stopwords  # 停用词库
import requests
from lxml import etree
from collections import Counter  # Counter类用于统计元素个数
from pyecharts import WordCloud


def brown01():
    # 查看brown语料库
    print(brown.readme())
    # 查看语料库所有句子个数
    print(len(brown.sents()))  # 57340
    # 查看语料库所有单词个数
    print(len(brown.words()))  # 1161192

def tokenize01():
    """英文分词处理"""
    text = "python is a high-level programming language and i like it!"
    # 分词处理
    seg_list = nltk.word_tokenize(text)
    print(seg_list)
    # 词性标注
    pos_list = nltk.pos_tag(seg_list)
    print(pos_list)

def jieba01():
    """中文分词处理"""
    str = "欢迎来到召唤师峡谷"
    # 1.全模式(适合词频统计): 将所有可能出现的词汇全部列出来,返回一个可迭代对象
    res1 = jieba.cut(str, cut_all=True)
    print(type(res1))  # <class 'generator'>
    print(list(res1))  # ['欢迎', '迎来', '来到', '召唤', '召唤师', '峡谷']
    # 2.精确模式(适合文本分析): 尽可能按语义进行分词处理
    res2 = jieba.cut(str, cut_all=False)
    print(list(res2))  # ['欢迎', '来到', '召唤师', '峡谷']
    # 3.搜索引擎模式(适合站内搜索)
    res3 = jieba.cut_for_search(str)
    print(res3)  # <generator object Tokenizer.cut_for_search at 0x0000026ADDD0C0F8>
    print("|".join(res3))  # 欢迎|来到|召唤|召唤师|峡谷

def stem01():
    # 1.PorterStemmer
    ps = PorterStemmer()
    print(type(ps))  # <class 'nltk.stem.porter.PorterStemmer'>
    # 词干提取
    print(ps.stem("looked"))  # look
    print(ps.stem("looking"))  # look
    # 2.SnowballStemmer
    print(SnowballStemmer.languages)  # 查看SnowballStemmer支持的语系
    ss = SnowballStemmer("english")  # 创建SnowballStemmer对象时必须指定语系
    print(type(ss))  # <class 'nltk.stem.snowball.SnowballStemmer'>
    # 词干提取
    print(ss.stem("looked"))  # look
    print(ss.stem("looking"))  # look
    # 3.LancasterStemme
    ls = LancasterStemmer()
    print(type(ls))  # <class 'nltk.stem.lancaster.LancasterStemmer'>
    # 词干提取
    print(ls.stem("looked"))  # look
    print(ls.stem("looking"))  # look

def lemmatize01():
    # 词性归并
    wl = WordNetLemmatizer()
    # 默认把所有词按名词处理
    print(wl.lemmatize("books"))  # book
    print(wl.lemmatize("cats"))  # cat
    print(wl.lemmatize("is"))  # is
    print(wl.lemmatize("went"))  # went
    # pos参数指定词性来做词形归并
    print(wl.lemmatize("is", pos="v"))  # be
    print(wl.lemmatize("are", pos="v"))  # be
    print(wl.lemmatize("went", pos="v"))  # go

def stopwords01():
    # 查看英文停用词库的单词
    res = stopwords.words("english")
    print(type(res))  # <class 'list'>
    print(res[:10])  # ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're"]
    text = "python is a high-level programming language, and i like it!"
    # 1.先做分词
    seg_list = nltk.word_tokenize(text)
    print(seg_list)  # ['Python', 'is', 'a', 'high-level', 'programming', 'language', ',', 'and', 'i', 'like', 'it', '!']
    # 2.再过滤停用词
    filter_list = [seg for seg in seg_list if seg not in stopwords.words("english")]
    print(filter_list)  # ['Python', 'high-level', 'programming', 'language', ',', 'like', '!']

def english():
    import nltk  # 分词模型和词性标注
    from nltk.stem import WordNetLemmatizer  # 词形归并语料库
    from nltk.corpus import stopwords  # 停用词语料库

    # 英文文本处理流程
    text = "The economic ills we suffer have come upon us over several decades. They will not go away in days, weeks," \
           " or months, but they will go away. They will go away because we, as Americans, have the capacity now, as " \
           "we have had in the past, to do whatever needs to be done to preserve this last and greatest bastion of " \
           "freedom."
    # 1.分词处理
    seg_list = nltk.word_tokenize(text)
    print(seg_list)
    # 2.词形归并处理
    wl = WordNetLemmatizer()
    word_list = [wl.lemmatize(seg) for seg in seg_list]
    print(word_list)
    # 3.停用词处理
    filter_list = [word for word in word_list if word not in stopwords.words("english")]
    print(filter_list)

class Chinese(object):
    """需求：爬取李克强政府工作报告内容并做词频统计"""
    def crawl(self):
        url = "http://www.gov.cn/premier/2017-03/16/content_5177940.htm"
        headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"}
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.content)
        p_list = html.xpath("//p | //span")
        data = ""
        for p in p_list:
            if p.text:
                data += p.text
        print(data)
        # 调用中文分词处理
        self.participle(data)

    def participle(self, data):
        # 1.分词处理
        seg_list = jieba.cut(data, cut_all=True)
        print(type(seg_list))  # <class 'generator'>
        # 读取中文停用词库
        file = "csv/中文停用词库.txt"
        # 将停用词库处理为列表
        stop_words = [line.strip() for line in open(file, encoding="utf-8")]
        print(stop_words)
        # 2.停用词处理
        words = [seg for seg in seg_list if seg not in stop_words and seg != ""]
        print(words)
        # 3.词频统计Counter(): 返回Counter({k1: v1, k2: v2, k3: v3...})并按value值降序排序
        counter = Counter(words)
        print(type(counter))  # <class 'collections.Counter'>
        print(counter)  # Counter({'发展': 134, '改革': 85, '经济': 71, '推进': 66...})
        # counter.most_common()将Counter({k1: v1, k2: v2...})转换成列表[(k1, v1),(k2, v2)...],参数n相当于topN
        res = counter.most_common(n=10)
        print(type(res))  # <class 'list'>
        print(res)  # [('发展', 134), ('改革', 85), ('经济', 71), ('推进', 66)...]
        # 调用绘制词云图方法
        self.draw(counter)

    def draw(self, counter):
        # 绘制词云图
        wc = WordCloud(title="李克强政府工作报告")
        wc.add("词频统计", counter.keys(), counter.values())
        wc.render("report.html")


if __name__ == '__main__':
    c = Chinese()
    c.crawl()


