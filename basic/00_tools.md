### tools
- [chrome无法添加应用、扩展程序和脚本](https://jingyan.baidu.com/article/f3ad7d0f09436709c3345b0b.html)
- [chrome安装谷歌访问助手](https://jingyan.baidu.com/article/7e440953191a2b2fc0e2ef0c.html)
- [chrome无法自动同步](https://post.smzdm.com/p/az59oog0/)
- [chrome安装谷歌访问助手程序包无效](https://blog.csdn.net/wst0717/article/details/88867047)
- [chrome固定到任务栏后点击出现两个图标](https://blog.csdn.net/qq_26012495/article/details/80814758)
- [chrome请停用以开发者模式运行的扩展程序](https://www.cnblogs.com/bky-zhwtt123/p/12671565.html)
- [github下载速度缓慢](https://www.jianshu.com/p/0493dcc15d6f)
- [fiddler设置只代理部分浏览器](https://segmentfault.com/q/1010000007944006)
- [fiddler手机数据抓包配置](https://www.cnblogs.com/qinyulin/articles/6843829.html)
- [fiddler设置代理后iphone有些app打不开](https://www.cnblogs.com/KK3228911/archive/2018/11/01/9890211.html)
- [jupyter代码自动补全](https://www.cnblogs.com/qiuxirufeng/p/9609031.html)
- [windows安装redis](https://www.jianshu.com/p/e16d23e358c0)
- [JetBrains全系列软件(插件)激活码](https://www.fuocu.cn/archives/jetbrains-crack/)
- [IDEA2020.2.x最新激活](http://www.cx1314.cn/article-419-1.html)
- [pycharm专业版永久激活](https://blog.csdn.net/weixin_39332299/article/details/79692283)
- [pycharm远程连接服务器调试代码](https://www.jianshu.com/p/79df9ac88e96)
- [pycharm删除项目](http://blog.csdn.net/xiaohukun/article/details/75077049)
- [pycharm导入外部模块](https://jingyan.baidu.com/article/93f9803f5dababe0e46f55fc.html)
- [pycharm安装black代码格式化](https://blog.csdn.net/u011510825/article/details/82287022)
- [tableau10.5破解版安装](https://www.jianshu.com/p/ec54bb870065)

### shortcut
```shell script
# Pycharm快捷键设置
File - Settings - Keymap
# 代码提示部分
m/f/v/c/p  # 方法/字段/变量/类/p参数
# 设置
Ctrl + Alt + S
# 代码格式化
Ctrl + Alt + L
# 查看函数详细注释
F2
# 取消sql语句高亮背景
File - Settings - Editor - Language Injections - 去掉勾选python: "SQL select/delete/insert/update/create"
```

### plugins
```shell script
# pycharm
Translation  # 翻译
Markdown Navigator  # 
Rainbow Brackets  # 彩虹括号
Material Theme UI  # 主题
Statistic  # 当前项目的统计信息
Mongo Plugin  # mongodb的可视化数据库工具  View --> Tool Windows --> Mongo Explorer
embedded web browser  # 内嵌浏览器

# chrome
谷歌访问助手
AdGuard                  # 广告拦截
Clear Cache              # 清空缓存
Extensity                # 管理chrome插件
Enhanced Github          # 显式github上文件大小
FeHelper                 # 前端助手
Git History              # 炫酷的展示github中任意文件的修改历史
Google translation       # 可保存单词本
Isometric Contributions  # 渲染github贡献记录的等距像素视图(装X神器)
JSONView                 # json格式化
Momentum                 # 壁纸
Octotree                 # 在github左侧显式当前工程目录结构
OneTab                   # 打开网页列表节约内存
Postman                  # 调试requests请求
Proxy SwitchyOmega       # fiddler代理
Smallpdf                 # pdf各种转换
Tab Activate             # 打开新标签页后自动跳转,chrome默认是不跳转的
Translate Man            # 翻译侠
uBlock Origin            # 网络请求过滤工具占用极低的内存和CPU
XPath Helper             # xpath助手
```

### sublime
```text
sublime左侧显示文件夹：直接将文件夹手动拖进来即可  
sublime转换大小写：Ctrl+KU、Ctrl+KL
sublime多个视图：view --> layout --> single/columns
[excel和csv区别](https://blog.csdn.net/weixin_39198406/article/details/78705016)
在某列末尾都加上逗号：B1=A1&","
```

### python
```text
- 编译性语言和解释性语言
编译性语言：源代码 - 编译器 - 一次性转换成可执行文件(效率高,不跨平台) - CPU
解释性语言：源代码 - 解释器 - 逐行解释运行代码(效率低,跨平台) - CPU
java既是编译性也是解释性语言,先编译成.class文件然后交给jvm运行,jvm是跨平台的,所以java跨平台的同时兼顾性能

- 线程的同步和异步？
线程同步：多个线程同时访问同一资源,要等待资源访问结束,浪费时间,效率低
线程异步：在访问资源时在空闲等待时同时访问其他资源,实现多线程机制  
- 网络的同步和异步？
同步：提交请求 > 等待服务器处理 > 处理完毕返回(期间浏览器不能干任何事)
异步: 请求通过事件触发->服务器处理(此时浏览器仍然可以干其他事)->处理完毕  
- 0、装饰器(重要)
- 1、TCP/UDP/HTTP协议区别？
- 2、深拷贝浅拷贝
- 3、简述一个前端请求的处理流程，在uwsgi/nginx/django之间的处理流程
- 4、redis用过哪些数据结构？怎么保存的
- 5、celery队列
- 6、modelfirst   dbfirst区别？
- 7、线程/进程/协程区别
- 8、tornado框架
- 9、向量化--one-hot编码/数据分箱
- 10、栈、堆
- 11、你知道的排序算法
- 12、MySQL优化、多表查询
- 13、Linux下找文件
- 14、闭包
- 15、Django模型类继承
- 16、时间更新模型类
- 17、Settings里面设置东西
- 18、ajax请求的csrf解决方法
- 19、机器数据分析/建模有什么感悟？
- 20、爬虫原理
- 30、redis为什么快？除了他是内存型数据库外，还有什么原因
- 31、python2和python3的区别？
- 32、你觉得python2的项目如果迁移到python3，困难会在哪里？- 

BIO/NIO/AIO   Netty框架
- kafka如何保证数据不丢失
- 线程池使用场景
- 数组去重,不使用工具类和set集合- BIO/NIO/AIO   Netty框架
- kafka如何保证数据不丢失
- 线程池使用场景
- 数组去重,不使用工具类和set集合
```

### 
```text
男人的温柔并不值钱,只有当这个男人足够强大之后,他的温柔才值钱
即使是一朵被踩烂的花,也有渴望阳光的权利如果你不想成为她的阳光,请把照耀她的机会让给别人
每次回头,都能看到身后每一个自己努力踏出的,参杂着血汗和泪水的,清晰而坚实的脚印.
爱情其实也不讲究什么合适不合适的,爱是稀里糊涂中招,旷日持久修炼,也许在你死去的那天,隔壁大妈嗑着瓜子说:这两人挺合适的嘛!
如果我没有见过满天的繁星,那么我也可以忍受无边的黑暗
人间烟火,心底波澜,几个人能免俗;江湖深远,顾盼流连,谁能了无牵挂
在承认自己傻逼的那一刻起,我才不再是傻逼
最主要的还是本质的善良,天性的温厚,开阔的胸襟,有了这三样,将来即使遇到大大小小的风波也不致演变成悲剧
人生如戏,全靠演技
生手怕熟手,熟手怕高手,高手怕失手
为你的难过而快乐的是敌人,为你的快乐而快乐的是朋友,为你的难过而难过的是那些该放心里的人
爱情经得起风雨而经不起平淡,友情经得起平淡而经不起风雨
不怕被利用,就怕没有用
我们应当尝试去打破一切的桎梏,而不是用这些桎梏来约束自己的思维在没有人用心陪伴的时候,读一本书,可能比做其它事更有益
岭深常得蛟龙在,梧高自有凤凰栖五十元人民币设计的再好看,也不如一百元招人喜欢
学会放弃眼前利益：有三个大小不一的西瓜,你吃哪个？
叶子飘落,不是因为风的召唤,而是树的舍弃
如果你要烧壶开水,生火到一半时发现柴不够,怎么办呢？为什么不把壶里的水倒掉一些？
人不会死于绝境,但往往栽在十字路口
切忌交浅言深,说话前你是主人,说话后你是仆人,许过的承诺一定要兑现,吹过的牛逼终究得实现
既憋不住尿,又憋不住话,是幼稚;只能憋住尿,却憋不住话,是不成熟;既能憋住尿,又能憋住话,是成熟;只能憋住话,却憋不住尿,说明你老了
并不是每天下班都能数星星,有时候也能看到日出
有为有不为,知足知不足;锐气藏于胸,和气浮于面;才气见于事,义气施于人
聪明的人千差万别,愚蠢的人有个共同点：总以为自己是聪明人
站在树上的鸟儿,从来不会害怕树枝断裂,因为她相信的不是树枝,而是她自己的翅膀
就好像一个小孩子突然要和一群大人做朋友,于是他小心翼翼地掏出兜里的玻璃球,这是他能想到的最贵重的东西
不是非得爬到山顶才能看见阳光,屋子亮了说明太阳已经出来了
碟子盛水自然不如碗,因为碟子是用来放大菜的
所谓情怀,就是不惜一切来追求和保护心中那份别人看似可笑的理想吧
趟浑水时记得穿双靴子
智商高是让自己高兴,情商高是让别人高兴,智商情商都不高,是自己不高兴,也不让别人高兴
在很年轻的时候就认清了自己想要的是什么,从而突破环境的限制甚至创造出有利于自己的环境来实现目标
人生浮光掠影,喜怒哀乐伤,皆为朝露时间潮涨潮落,跌宕起伏平,亦是轻风
别人捧你骂你赞你毁你,只不过是闲暇时凑个热闹,他们转头就忘,你何必放不下,过份抬举彼此,实则泯然众人矣,生活本就如此,脚踏实地便好
喂！妖妖灵吗？我他妈又翻车了！不是上次那个弯道,这次我连方向盘都转丢了
人与人之间差距太大,但距离又太小
自我提升、博闻广识、眼界格局、家庭和睦、结交朋友都比年轻时候攒那么点钱重要过去+现在=未来
太可怕了,想想去年这时候我还是25岁
人这一辈子最难的就是摆正自己的位置
人生是投资和收益的人生,如果你有钱,那就投入钱,没有钱可以投入能力和经验,没有能力和经验的话,还可以投入热情,勤奋和努力,如果连这个都没有,那还是算了
永远尽可能准备好资源,随时准备抓住机会
给别人的比别人期待的多一点
赚钱的普遍法则：多做,快做,变着花样做,就是别跟着别人一样做
心中曾经执剑的少年,如今也混迹于市井
人的一生,都是在选择中度过,大部分时候,你并不能在好与坏中选择好,而是在坏与更坏中选择坏
那并不是我的花,我只是刚好途径了她的绽放;
听的比想得多,想的比说的多,说得比做得多;学不吃苦,玩不出花,一辈子庸庸碌碌;
社会发展太快 ,人的欲望提高了,生活成本提高了,对未来的期望提高了,希望一下子破灭就会悲剧,人很多时候绝望并不是因为走投无路,而是因为对未来的幻灭;
期待落空的那一天,收拾好碎一地的玻璃心渣子,也还是要向前走;
水往低处流,人往高处走：比如你家漏水了,楼下邻居就会上来找你;
睡前喝一袋牛奶,会比不喝牛奶的情况下,多花几块钱;
早晨起来,喝上一大杯白开水,并不能成为迟到的理由;
据德国科学家研究得出结论,一个成年男子每吸烟60秒就会减少一分钟的寿命;
她那时还年轻,不知道命运赠送的礼物,早已在暗中标好了价格
曾以为走不出的日子,现在都回不去了 -- 村上春树
构建故事需要正面与反面的角色,这样简单的标签化简化了思考的难度,也可以在短时间内带动人们的情绪
养狗的人都会说自己家的狗不咬人
```