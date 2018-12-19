# coding=utf-8
"""
NLTK是Python自然语言处理的一个工具包
分类: 根据词性来分(词性标注);名词、形容词、动词等...
分词: 根据语义来分
"""

import nltk
# 调用nltk的包管理工具,可以下载语料库和模型等数据;其中Brown语料库、Punkt分词模型是必装的
# nltk.download()


def test01():
    # 导入布朗大学语料库
    from nltk.corpus import brown

    # 查看brown语料库
    print(brown.readme())
    # 查看语料库所有句子个数
    print(len(brown.sents()))  # 57340
    # 查看语料库所有单词个数
    print(len(brown.words()))  # 1161192


def test02():
    """
    英文分词: seg_list = nltk.word_tokenize(text)
    词性标注: pos_list = nltk.pos_tag(seg_list)
    """

    # 文本样例
    text = "python is a high-level programming language, and i like it!"

    # 分词处理(需实现安装好punkt分词模型): 返回所有词的列表
    seg_list = nltk.word_tokenize(text)
    print(type(seg_list))  # <class 'list'>
    print(seg_list)  # ['Python', 'is', 'a', 'high-level', 'programming', 'language', ',', 'and', 'i', 'like', 'it', '!']

    # 词性标注
    pos_list = nltk.pos_tag(seg_list)
    print(pos_list)  # [('Python', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('high-level', 'JJ'), ('programming', 'NN'), ('language', 'NN'), (',', ','), ('and', 'CC'), ('i', 'VBP'), ('like', 'IN'), ('it', 'PRP'), ('!', '.')]


def test03():
    """
    中文分词: res = jieba.cut(text, cut_all=True)
    词性标注: words = jieba.posseg.cut.md(text)
    """

    # jieba专门用来处理中文分词
    import jieba
    # import jieba.posseg as pseg

    # 原文本
    text = "欢迎来到召唤师峡谷"

    # 1、全模式(适合词频统计): 将所有可能出现的词汇全部列出来,返回一个可迭代对象
    res1 = jieba.cut(text, cut_all=True)
    print(type(res1))  # <class 'generator'>
    # 转换成list格式
    print(list(res1))  # ['欢迎', '迎来', '来到', '召唤', '召唤师', '峡谷']

    # 2、精确模式(适合文本分析): 尽可能按语义进行分词处理
    res2 = jieba.cut(text, cut_all=False)
    print(list(res2))  # ['欢迎', '来到', '召唤师', '峡谷']

    # 3、搜索引擎模式(适合站内搜索)
    res3 = jieba.cut_for_search(text)
    print(res3)  # <generator object Tokenizer.cut_for_search at 0x0000026ADDD0C0F8>
    print("|".join(res3))  # 欢迎|来到|召唤|召唤师|峡谷

    # 词性标注
    # words = pseg.cut.md("我叫钢蛋，来自蒙塔基")
    # print(type(words))  # <class 'generator'>
    # for word, flag in words:
    #     print("%s: %s" % (word, flag), end=" & ")
    #     # 我: r & 叫: v & 钢蛋: n & ，: x & 来自: v & 蒙: v & 塔基: nrt &


def test04():
    """
    词干提取
    """

    # 1、PorterStemmer
    from nltk.stem.porter import PorterStemmer

    # 创建PorterStemmer对象
    ps = PorterStemmer()
    print(type(ps))  # <class 'nltk.stem.porter.PorterStemmer'>
    print(ps)  # <PorterStemmer>

    # 词干提取
    print(ps.stem("looked"))  # look
    print(ps.stem("looking"))  # look

    # 2、SnowballStemmer
    from nltk.stem.snowball import SnowballStemmer

    # 查看SnowballStemmer支持的语系
    print(SnowballStemmer.languages)  # ('arabic', 'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'norwegian', 'porter', 'portuguese', 'romanian', 'russian', 'spanish', 'swedish')

    # 创建SnowballStemmer对象: 必须先指定语系
    ss = SnowballStemmer("english")
    print(type(ss))  # <class 'nltk.stem.snowball.SnowballStemmer'>
    print(ss)  # <nltk.stem.snowball.SnowballStemmer object at 0x00000272DA64AC50>

    # 词干提取
    print(ss.stem("looked"))  # look
    print(ss.stem("looking"))  # look

    # 3、LancasterStemme
    from nltk.stem.lancaster import LancasterStemmer

    # 创建LancasterStemmer对象
    ls = LancasterStemmer()
    print(type(ls))  # <class 'nltk.stem.lancaster.LancasterStemmer'>
    print(ls)  # <LancasterStemmer>

    # 词干提取
    print(ls.stem("looked"))  # look
    print(ls.stem("looking"))  # look


def test05():
    """
    词形归并: wl = WordNetLemmatizer()
             wl.lemmatize("***")
    """

    # 需事先安装好wordnet语料库
    from nltk.stem import WordNetLemmatizer

    # 创建WordNetLemmatizer对象
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


def test06():
    """
    停用词处理: stopwords.words("language")
    """

    # 导入停用词库
    from nltk.corpus import stopwords

    # 查看英文停用词库的单词
    res = stopwords.words("english")
    print(type(res))  # <class 'list'>
    print(res[:10])  # ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're"]

    # 文本样例
    text = "python is a high-level programming language, and i like it!"

    # 1、先做分词
    seg_list = nltk.word_tokenize(text)
    print(seg_list)  # ['Python', 'is', 'a', 'high-level', 'programming', 'language', ',', 'and', 'i', 'like', 'it', '!']

    # 2、再过滤停用词
    filter_list = [seg for seg in seg_list if seg not in stopwords.words("english")]
    print(filter_list)  # ['Python', 'high-level', 'programming', 'language', ',', 'like', '!']


# 英文文本域处理流程
def english():
    # 分词模型和词性标注
    import nltk
    # 词形归并语料库
    from nltk.stem import WordNetLemmatizer
    # 停用词语料库
    from nltk.corpus import stopwords

    # 文本
    text = "The economic ills we suffer have come upon us over several decades. They will not go away in days, weeks," \
           " or months, but they will go away. They will go away because we, as Americans, have the capacity now, as " \
           "we have had in the past, to do whatever needs to be done to preserve this last and greatest bastion of " \
           "freedom."

    # 1、分词处理
    seg_list = nltk.word_tokenize(text)
    print(seg_list)

    # 2、词形归并处理
    wl = WordNetLemmatizer()
    word_list = [wl.lemmatize(seg) for seg in seg_list]
    print(word_list)

    # 3、停用词处理
    filter_list = [word for word in word_list if word not in stopwords.words("english")]
    print(filter_list)


if __name__ == "__main__":
    test01()
    # test02()
    # test03()
    # test04()
    # test05()
    # test06()
    # english()
