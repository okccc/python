# coding=utf-8
"""
参考文档：http://pyecharts.org/#/zh-cn/charts_base
pyecharts绘图步骤：
1.bar =Bar(title="") --> 初始化具体图表类型
2.bar.add(...) --> 添加数据及配置项(name="",x_axis=attr,y_axis=value...)
# show_config() --> 打印输出图表的配置项
3.render(path="") --> 生成html文件,需使用浏览器打开
"""

import numpy as np

def bar01():
    # 柱形图Bar
    from pyecharts import Bar
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    value1 = np.random.randint(10, 50, 6)
    value2 = np.random.randint(10, 50, 6)
    # 初始化图表
    bar = Bar(title="柱状图示例", subtitle="...")
    # 添加数据配置
    bar.add(name="商家A", x_axis=attr, y_axis=value1, is_stack=False)  # is_stack：是否将数据堆叠
    bar.add(name="商家B", x_axis=attr, y_axis=value2, is_stack=False)
    # 渲染图表
    bar.render(path="D://PycharmProjects/python/analysis/csv/bar01.html")
    bar = Bar(title="标记线和标记点示例")
    bar.add(name="商家A", x_axis=attr, y_axis=value1, mark_point=["average"])  # mark_point：标记点
    bar.add(name="商家B", x_axis=attr, y_axis=value2, mark_line=["min", "max"])  # mark_line：标记线
    bar.render(path="D://PycharmProjects/python/analysis/csv/bar02.html")
    bar = Bar(title="x 轴和 y 轴交换")
    bar.add(name="商家A", x_axis=attr, y_axis=value1)
    bar.add(name="商家B", x_axis=attr, y_axis=value2, is_convert=True)  # is_convert：是否行列转换
    bar.render(path="D://PycharmProjects/python/analysis/csv/bar03.html")

def line01():
    # 折线图Line
    from pyecharts import Line
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    value1 = np.random.randint(10, 50, 6)
    value2 = np.random.randint(10, 50, 6)
    line = Line(title="折线图示例")
    line.add(name="商家A", x_axis=attr, y_axis=value1, mark_point=["average"])
    line.add(name="商家B", x_axis=attr, y_axis=value2, mark_line=["average", "max"], is_smooth=True)  # is_smooth：是否平滑曲线显示
    line.render(path="D://PycharmProjects/python/analysis/csv/line01.html")
    line = Line("折线图示例")
    line.add("商家A", attr, value1, mark_point=["average"],mark_point_symbol='diamond',  # mark_point_symbol：标记点的形状
             mark_point_textcolor='black')  # mark_point_textcolor：标记点的字体颜色
    line.add("商家B", attr, value2, mark_point=["average"], mark_point_symbol='arrow',
             mark_point_symbolsize=40)  # mark_point_symbolsize：标记点的大小
    line.render(path="D://PycharmProjects/python/analysis/csv/line02.html")
    line = Line("折线图-阶梯图示例")
    line.add("商家A", attr, value1, is_step=True, is_label_show=True)  # is_step：是否是阶梯线图
    line.add("商家B", attr, value2, is_step=True, is_label_show=True)  # is_label_show：是否显示标签
    line.render(path="D://PycharmProjects/python/analysis/csv/line03.html")
    line = Line("折线图-面积图示例")
    line.add("商家A", attr, value1, is_fill=True,  # is_fill：是否填充曲线所绘制面积
             line_opacity=0.2,  # line_opacity=0.2：线条的不透明度
             area_opacity=0.4,  # area_opacity：填充区域的透明度
             symbol=None)  # symbol：图形
    line.add("商家B", attr, value2, is_fill=True, area_color='#000', area_opacity=0.3, is_smooth=True)  # area_color：填充区域的颜色
    line.render(path="D://PycharmProjects/python/analysis/csv/line04.html")

def scatter01():
    # 散点图Scatter
    from pyecharts import EffectScatter
    value1 = [10, 20, 30, 40, 50, 60]
    value2 = [25, 20, 15, 10, 60, 33]
    es = EffectScatter(title="动态散点图示例")  # 带有涟漪特效动画
    es.add(name="effectScatter", x_axis=value1, y_axis=value2)
    es.render(path="D://PycharmProjects/python/analysis/csv/scatter01.html")
    es = EffectScatter("动态散点图各种图形示例")  # symbol_size：标记图形大小
    es.add("", [10], [10], symbol_size=20, effect_scale=3.5, effect_period=3, symbol="pin")  # 大头针
    es.add("", [20], [20], symbol_size=15, effect_scale=4.5, effect_period=4, symbol="rect")  # 矩形
    es.add("", [30], [30], symbol_size=15, effect_scale=5.5, effect_period=5, symbol="roundRect")  # 圆角矩形
    es.add("", [40], [40], symbol_size=15, effect_scale=6.5, effect_brushtype='fill', symbol="diamond")  # 菱形
    es.add("", [50], [50], symbol_size=20, effect_scale=2.5, effect_period=3, symbol="triangle")  # 三角形
    es.add("", [60], [60], symbol_size=10, effect_scale=5.5, effect_period=3, symbol="arrow")  # 箭头
    es.render(path="D://PycharmProjects/python/analysis/csv/scatter02.html")

def funnel01():
    # 漏斗图Funnel
    from pyecharts import Funnel
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    value = [20, 40, 60, 80, 100, 120]
    funnel = Funnel(title="漏斗图示例")
    funnel.add("商品", attr, value, is_label_show=True, label_pos="inside", label_text_color="#fff")
    funnel.render(path="D://PycharmProjects/python/analysis/csv/funnel.html")

def gauge01():
    # 仪表盘Gauge
    from pyecharts import Gauge
    gauge = Gauge(title="仪表盘示例")
    gauge.add(name="业务指标", attr="完成率", value=66.66)
    gauge.render(path="D://PycharmProjects/python/analysis/csv/gauge.html")

def liquid01():
    # 水球图Liquid
    from pyecharts import Liquid
    liquid = Liquid(title="水球图示例")
    liquid.add(name="Liquid", data=[0.6])
    liquid.render(path="D://PycharmProjects/python/analysis/csv/liquid01.html")
    liquid = Liquid(title="水球图示例")
    liquid.add(name="Liquid", data=[0.6, 0.5, 0.4, 0.3], is_liquid_outline_show=False)  # is_liquid_outline_show：是否显示边框
    liquid.render(path="D://PycharmProjects/python/analysis/csv/liquid02.html")
    liquid = Liquid(title="水球图示例")
    liquid.add(name="Liquid", data=[0.6, 0.5, 0.4, 0.3], is_liquid_animation=False, shape='diamond')  # is_liquid_animation：是否显示波浪动画
    liquid.render(path="D://PycharmProjects/python/analysis/csv/liquid03.html")

def pie01():
    # 饼图Pie
    from pyecharts import Pie
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    value = np.random.randint(10, 100, 6)
    pie = Pie(title="饼图示例")
    pie.add("", attr, value, is_label_show=True)
    pie.render(path="D://PycharmProjects/python/analysis/csv/pie01.html")
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    value1 = [10, 20, 30, 40, 50, 60]
    value2 = [10, 20, 30, 40, 50, 60]
    pie = Pie(title="饼图-玫瑰图示例", title_pos='center', width=900)
    pie.add("商品A", attr, value1, center=[25, 50], is_random=True, radius=[30, 75],  # center：饼图圆心坐标  radius：饼图半径
            rosetype='radius')  # rosetype：是否展示成南丁格尔图,通过半径区分数据大小
            # rosetype='radius'：扇区圆心角展现数据的百分比,半径展现数据大小;  rosetype='area'：所有扇区圆心角相同,仅通过半径展现数据大小
    pie.add("商品B", attr, value2, center=[75, 50], is_random=True, radius=[30, 75], rosetype='area',
            is_legend_show=False, is_label_show=True)
    pie.render(path="D://PycharmProjects/python/analysis/csv/pie02.html")
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [11, 12, 13, 10, 10, 10]
    pie = Pie(title="饼图-圆环图示例", title_pos='center')
    pie.add("", attr, v1, radius=[40, 75], label_text_color=None,
                is_label_show=True,
                legend_orient='vertical',  # 图例展开的方向
                legend_pos='left')  # 图例的位置
    pie.render(path="D://PycharmProjects/python/analysis/csv/pie03.html")

def radar01():
    # 雷达图Radar
    from pyecharts import Radar
    schema = [
        ("销售", 6500), ("管理", 16000), ("信息技术", 30000),
        ("客服", 38000), ("研发", 52000), ("市场", 25000)
    ]
    v1 = [[4300, 10000, 28000, 35000, 50000, 19000]]
    v2 = [[5000, 14000, 28000, 31000, 42000, 21000]]
    radar = Radar(title="雷达图示例")
    radar.config(schema)
    radar.add("预算分配", v1, is_splitline=True,  # is_splitline：是否显示分割线
              is_axisline_show=True)  # is_axisline_show：是否显示坐标轴线
    radar.add("实际开销", v2, label_color=["#4e79a7"], is_area_show=False,  # is_area_show：是否显示填充区域
              legend_selectedmode='single')
    radar.render(path="D://PycharmProjects/python/analysis/csv/radar.html")

def word_cloud():
    # 词云图WordCloud
    from pyecharts import WordCloud
    attr = ['Python', 'Java', '大数据', '数据分析', '可视化',
            '人工智能', '自然语言处理', '数据挖掘', '机器学习', 'Hadoop', 'Spark',
            'TensorFlow', 'web前段', '自动化运维', 'php', 'Linux', 'JavaScript', '爬虫', '算法', '物联网']
    value = [100, 75, 65, 55, 23, 22, 45, 40, 35, 30, 25, 20, 18, 16, 13, 10, 9, 6, 3, 1]
    # value = np.random.randint(10, 50, 20)
    wc = WordCloud(title="绘制词云图", width=1000, height=500)
    wc.add("程序员", attr, value, word_size_range=[20, 100])  # word_size_range：单词字体大小范围
    wc.render(path="D://PycharmProjects/python/analysis/csv/wordcloud.html")
word_cloud()

def heat_map():
    # 热力图HeatMap
    from pyecharts import HeatMap
    import random
    x_axis = ["12a", "1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12p", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p"]
    y_aixs = ["Saturday", "Friday", "Thursday", "Wednesday", "Tuesday", "Monday", "Sunday"]
    data = [[i, j, random.randint(0, 50)] for i in range(24) for j in range(7)]
    hm = HeatMap(title="热力图示例")
    hm.add("热力图直角坐标系", x_axis, y_aixs, data, is_visualmap=True, visual_text_color="#000", visual_orient='horizontal')
    hm.render(path="D://PycharmProjects/python/analysis/csv/heatmap.html")

def geo01():
    # 地理坐标系Geo
    from pyecharts import Geo
    data = [("海门", 9),("鄂尔多斯", 12),("招远", 12),("舟山", 12),("齐齐哈尔", 14),("盐城", 15),("赤峰", 16),("青岛", 18),("乳山", 18),("金昌", 19),("泉州", 21),("莱西", 21),("日照", 21),("胶南", 22),("南通", 23),("拉萨", 24),("云浮", 24),("梅州", 25),("文登", 25),("上海", 25),("攀枝花", 25),("威海", 25),("承德", 25),("厦门", 26),("汕尾", 26),("潮州", 26),("丹东", 27),("太仓", 27),("曲靖", 27),("烟台", 28),("福州", 29),("瓦房店", 30),("即墨", 30),("抚顺", 31),("玉溪", 31),("张家口", 31),("阳泉", 31),("莱州", 32),("湖州", 32),("汕头", 32),("昆山", 33),("宁波", 33),("湛江", 33),("揭阳", 34),("荣成", 34),("连云港", 35),("葫芦岛", 35),("常熟", 36),("东莞", 36),("河源", 36),("淮安", 36),("泰州", 36),("南宁", 37),("营口", 37),("惠州", 37),("江阴", 37),("蓬莱", 37),("韶关", 38),("嘉峪关", 38),("广州", 38),("延安", 38),("太原", 39),("清远", 39),("中山", 39),("昆明", 39),("寿光", 40),("盘锦", 40),("长治", 41),("深圳", 41),("珠海", 42),("宿迁", 43),("咸阳", 43),("铜川", 44),("平度", 44),("佛山", 44),("海口", 44),("江门", 45),("章丘", 45),("肇庆", 46),("大连", 47),("临汾", 47),("吴江", 47),("石嘴山", 49),("沈阳", 50),("苏州", 50),("茂名", 50),("嘉兴", 51),("长春", 51),("胶州", 52),("银川", 52),("张家港", 52),("三门峡", 53),("锦州", 54),("南昌", 54),("柳州", 54),("三亚", 54),("自贡", 56),("吉林", 56),("阳江", 57),("泸州", 57),("西宁", 57),("宜宾", 58),("呼和浩特", 58),("成都", 58),("大同", 58),("镇江", 59),("桂林", 59),("张家界", 59),("宜兴", 59),("北海", 60),("西安", 61),("金坛", 62),("东营", 62),("牡丹江", 63),("遵义", 63),("绍兴", 63),("扬州", 64),("常州", 64),("潍坊", 65),("重庆", 66),("台州", 67),("南京", 67),("滨州", 70),("贵阳", 71),("无锡", 71),("本溪", 71),("克拉玛依", 72),("渭南", 72),("马鞍山", 72),("宝鸡", 72),("焦作", 75),("句容", 75),("北京", 79),("徐州", 79),("衡水", 80),("包头", 80),("绵阳", 80),("乌鲁木齐", 84),("枣庄", 84),("杭州", 84),("淄博", 85),("鞍山", 86),("溧阳", 86),("库尔勒", 86),("安阳", 90),("开封", 90),("济南", 92),("德阳", 93),("温州", 95),("九江", 96),("邯郸", 98),("临安", 99),("兰州", 99),("沧州", 100),("临沂", 103),("南充", 104),("天津", 105),("富阳", 106),("泰安", 112),("诸暨", 112),("郑州", 113),("哈尔滨", 114),("聊城", 116),("芜湖", 117),("唐山", 119),("平顶山", 119),("邢台", 119),("德州", 120),("济宁", 120),("荆州", 127),("宜昌", 130),("义乌", 132),("丽水", 133),("洛阳", 134),("秦皇岛", 136),("株洲", 143),("石家庄", 147),("莱芜", 148),("常德", 152),("保定", 153),("湘潭", 154),("金华", 157),("岳阳", 169),("长沙", 175),("衢州", 177),("廊坊", 193),("菏泽", 194),("合肥", 229),("武汉", 273),("大庆", 279),]
    geo = Geo(title="全国主要城市空气质量", subtitle="data from pm2.5", title_color="#fff", title_pos="center",
    width=1200, height=600, background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add("", attr, value, visual_range=[0, 200], visual_text_color="#fff", symbol_size=15, is_visualmap=True)
    geo.render(path="D://PycharmProjects/python/analysis/csv/geo01.html")
    geo = Geo(title="全国主要城市空气质量", subtitle="data from pm2.5", title_color="#fff", title_pos="center", width=1200, height=600,
    background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add("", attr, value, type="heatmap", is_visualmap=True, visual_range=[0, 300], visual_text_color='#fff')
    geo.render(path="D://PycharmProjects/python/analysis/csv/geo02.html")
    data = [("海门", 9), ("鄂尔多斯", 12), ("招远", 12), ("舟山", 12), ("齐齐哈尔", 14), ("盐城", 15)]
    geo = Geo("全国主要城市空气质量", "data from pm2.5", title_color="#fff", title_pos="center",
              width=1200, height=600, background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add("", attr, value, type="effectScatter", is_random=True, effect_scale=5)
    geo.render(path="D://PycharmProjects/python/analysis/csv/geo03.html")

def map01():
    # 地图Map
    from pyecharts import Map
    attr = ["福建", "山东", "北京", "上海", "甘肃", "新疆", "河南", "广西", "西藏"]
    value = [155, 10, 66, 78, 33, 80, 190, 53, 49.6]
    map = Map(title="Map 结合 VisualMap 示例", width=1200, height=600)
    map.add("", attr, value, maptype='china', is_visualmap=True, visual_text_color='#000')
    map.render(path="D://PycharmProjects/python/analysis/csv/map01.html")
    attr = ['汕头市', '汕尾市', '揭阳市', '阳江市', '肇庆市']
    value = [20, 190, 253, 77, 65]
    map = Map(title="广东地图示例", width=1200, height=600)
    map.add("", attr, value, maptype='广东', is_visualmap=True, visual_text_color='#000')
    map.render(path="D://PycharmProjects/python/analysis/csv/map02.html")

