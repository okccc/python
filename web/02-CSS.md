# CSS介绍

CSS(Cascading Style Sheets)通常称为CSS样式表或层叠样式表（级联样式表），主要用于设置HTML页面中的文本内容（字体、大小、对齐方式等）、图片的外形（宽高、边框样式、边距等）以及版面的布局等外观显示样式                           



# CSS字体样式

```css
h2 {
    /* 字体大小 */
    font-size: 14px;  
    
    /* 字体样式：为了避免unicode编码问题可使用\5FAE\8F6F\96C5\9ED1代替中文 */
    font-family: "微软雅黑";  
    
    /* 字体粗细：400是normal  700是bold */
    font-weight: 700;  
    
    /* 字体风格：normal正常值  italic斜体 */
    font-style: normal;  
    
    /* font综合设置字体样式：font: font-style font-weight font-size font-family */
    font: normal bold 14px "微软雅黑";
    /* 不需要的属性可以不写,但必须保留font-size和font-family */
    font: 14px "微软雅黑";
    
    /* 文本装饰 none | overline(下划线) | ubderline(上划线) | line-through(穿过文本的线) */
    text-decoration: none; /* 常用于a链接*/
}
```



# CSS基础选择器（重点）

要将CSS样式应用于特定的HTML元素，首先需要找到该目标元素

## 标签选择器

优点：一次性为所有同类型标签统一样式，同时也是他的缺点，不能差异化设置样式

```
标签名 {属性1:属性值1; 属性2:属性值2; 属性3:属性值3; }  
p {   
	color: pink;
}
div {
	color: purple;
}
```

## 类选择器

```css
.类名 {属性1:属性值1; 属性2:属性值2; 属性3:属性值3; }
span {
	font-size: 100px;
}
.blue {
	color: blue;
}
.red {
	color: red;
}

<span class="blue">G</span>
<span class="red">o</span>
/*多类名选择器在后期布局比较复杂的情况下使用*/
<div class="pink fontWeight font20">亚瑟</div>
<div class="font20">刘备</div>
<div class="font14 pink">安其拉</div>
<div class="font14">貂蝉</div>
```
### 1. 链接伪类选择器

- :link      /* 未访问的链接 */
- :visited   /* 已访问的链接 */
- :hover     /* 鼠标移动到链接上 */
- :active    /* 选定的链接，点击鼠标不松开 */


   注意写的时候，他们的顺序尽量不要颠倒  按照  lvha 的顺序

~~~css
/*类选择器是一个点，比如 .demo {}   伪类选择器是2个点就是冒号，比如  :link{}*/
a {   
    font-weight: 700;
    font-size: 16px;
    color: gray;
}
/*实际开发只写a:hover{}就可以，其它3个不需要*/
a:hover {   
    color: red; 
}

<a href="#"> 秒杀 </a>
~~~

### 2. 结构伪类选择器

- :first-child : 匹配属于其父元素的首个子元素的指定选择器
- :last-child : 匹配属于其父元素的最后一个子元素的指定选择器
- :nth-child(n) : 匹配属于其父元素的第 N 个子元素，不论元素的类型
- :nth-last-child(n) : 匹配属于其父元素的第 N 个子元素，不论元素的类型，倒序

~~~css
li:first-child { /*  第一个字标签 */
        		color: pink; 
        	}
li:last-child {   /* 最后一个字标签 */
        		color: purple;
        	}
li:nth-child(4) {   /* 第n个字标签 */ 
				color: skyblue;
        	}
li:nth-child(odd) {  /* 所有的 odd奇数 子标签 */
				color: pink;
        	}
li:nth-child(even) {    /* 选择所有的 even偶数 子标签 */
				color: deeppink;
        	} 
li:nth-child(3n) {   /* 指定公式选择子标签 */
				color: pink;  
        	}
~~~

### 3. 目标伪类选择器

 :target目标伪类选择器，选取当前活动的目标元素（比如锚点跳转到的目标标签）

~~~css
:target {
		color: red;
		font-size: 30px;
}
~~~

## id选择器

```css
#id名 {属性1:属性值1; 属性2:属性值2; 属性3:属性值3; }
#big {
	color: pink;
}

<div id="big">熊大</div>
```

W3C标准规定一个页面内不允许有相同名字的id出现，但是允许相同名字的class

所以类选择器（名字）可以多次重复使用；id选择器（身份证号码）只能使用一次

## 通配符选择器（不常用）

通配符选择器用“*”号表示，是所有选择器中作用范围最广的，能匹配页面中所有元素

```css
* { 属性1:属性值1; 属性2:属性值2; 属性3:属性值3; }
* {
  margin: 0;                    /* 定义外边距*/
  padding: 0;                   /* 定义内边距*/
```



# CSS外观属性

```css
p {
    /*文本颜色 推荐使用十六进制#FF0000 */
    color: red;  
    
    /* 行间距 一般行距比字号大7.8像素左右就可以了 */
	line-height: 26px;  
    
    /* 文字居中对齐 */
    text-align: center;  
    
    /* 首行缩进 2em就是2个汉字的宽度 */
	text-indent: 2em;  
    
    /* 字间距 */
    letter-spacing: 2px;  
    
    /* 单词间距 */
    word-spacing: 10px;  
    
    /* 颜色半透明rgba(r,g,b,a)：a是alpha透明的意思 取值范围 0~1之间 */
    color: rgba(0,0,0,0.3)  
        
    /* 文字阴影text-shadow：水平位置 垂直位置 模糊距离 阴影颜色(前两个参数必须, 后两个参数可省略) */
    text-shadow: 5px 11px 3px rgba(0,0,0,0.5);  
}
```



# sublime快捷方式

1. 生成标签 直接输入标签名 按tab键即可   比如  div   然后tab 键， 就可以生成 <div></div>

2. 如果想要生成多个相同标签  加上 * 就可以了 比如   div*3  就可以快速生成3个div

3. 如果有父子级关系的标签，可以用 >  比如   ul > li就可以了

4. 如果有兄弟关系的标签，用  +  就可以了 比如 div+p  

5. 如果生成带有类名或者id名字的，  直接写  .demo  或者  #two   tab 键就可以了

   

# CSS样式表

CSS可以写到那个位置？ 是不是一定写到html文件里面呢？

## 行内式

是通过标签的style属性来设置元素的样式

```css
<div style="color: pink; ">今天很期待学习CSS</div>
```

## 内部样式表

将CSS代码集中写在HTML文档的head头部标签中

```html
<head>
    <style type="text/CSS">
        选择器 {属性1:属性值1; 属性2:属性值2; 属性3:属性值3;}
    </style>
</head>
```

## 外部样式表（推荐）

将所有的样式放在以.CSS为扩展名的文件中，通过link标签链接到HTML文档中

```html
<head>
  <link href="CSS文件的路径" type="text/CSS" rel="stylesheet" />
</head>
```



# 标签类型（display）

HTML标签一般分为块标签和行内标签两种类型，它们也称块元素和行内元素

## 块标签（block-level）

块元素会独自占据一整行或多整行，可以设置宽度、高度、对齐等属性，常用于网页布局和网页结构

常见块元素<h1>~<h6>、<p>、<div>、<ul>、<ol>、<li>等，其中<div>标签最典型
特点：
1.总是从新行开始
2.行高、外边距以及内边距都可以控制。
3.宽度默认是容器的100%
4.可以容纳内联元素和其他块元素。
注意：只有文字才能组成段落，因此p里面不能放块级元素，h1~h6、dt等标签同理

## 行内标签（inline-level）

行内元素不占有独立的区域，不可以设置宽度、高度、对齐等属性，常用于控制页面中文本的样式

常见行内元素<a>、<strong>、<b>、<em>、<i>、<del>、<s>、<ins>、<u>、<span>等，其中<span>标签最典型
特点：
1.和相邻行内元素在一行上。
2.高、宽无效，但水平方向的padding和margin可以设置，垂直方向的无效。
3.默认宽度就是它本身内容的宽度。
4.行内元素只能容纳文本或则其他行内元素。

## 行内块标签（inline-block）

行内元素中有几个特殊的标签<img />、<input />、<td>，可以设置宽高和对齐属性，称之为行内块元素。
特点：
1.和相邻行内元素（行内块）在一行上,但是之间会有空白缝隙。
2.默认宽度就是它本身内容的宽度。
3.高度，行高，外边距以及内边距都可以控制。

```css
/* 标签类型转换 */
div {
    width: 100px;
    height: 100px;
    background-color: pink;
    /* 块标签转为行内标签模式 */
    display: inline;  
}
span {
    width: 100px;
    height: 100px;
    background-color: hotpink;
    /* 行内标签转为块标签模式 */
    display: block;  
}
a {
    width: 50px;
    height: 20px;
    background-color: deeppink;
    /* 行内标签转为行内块标签模式 */
    display: inline-block;  
}
```



# CSS复合选择器

复合选择器是由两个或多个基础选择器，通过不同的方式组合而成的

## 交集选择器

交集选择器由两个选择器构成，第一个为标签选择器，第二个为class选择器，两个选择器之间不能有空格

~~~css
/* p.red选择的是类名为.red的段落标签  */
p.red {
	font-size:  30px;
}
         
<p class="red">小强</p>
~~~

## 并集选择器

并集选择器由各个选择器通过<strong style="color:#f00">逗号</strong>连接而成，如果某些选择器定义的样式完全相同，可以集体声明

~~~css
/* div,p,span,.daye表示将这些个标签统一设置成蓝色 */ 
div,p,span,.daye {
    color:blue;
    font-size: 18px;
}

<div>刘德华</div>
<p>张学友</p>
<span>郭富城</span>
<h1 class="daye">凤大爷</h1>
~~~

## 后代选择器

外层标签写在前面，内层标签写在后面，中间用空格分隔

```css
/* .jianlin p表示类名为jianlin的标签的字标签p */
.jianlin p {
    color: red;
}

<p>王者荣耀</p>
<div class="jianlin">
	<p>王思聪</p>
</div>
```

## 子元素选择器

父级标签写在前面，子级标签写在后面，中间用一个 &gt; 进行连接

~~~css
/*  空格 后代选择器, 可以选择儿子 孙子 重孙子.. */
.nav li { 
	color: red;
		}
/* > 子元素选择器,只选择儿子 */
.nav > li {  
    color: pink;
}

<ul class="nav">
    <li>一级菜单
        <ul>
            <li>二级菜单</li>
            <li>二级菜单</li>
            <li>二级菜单</li>
        </ul>
    </li>
</ul>
~~~

## 属性选择器

| 属性选择器             |  含义           |
| -------------------  |  -------------- |
| Selector[attr]       | 存在attr属性     |
| Selector[attr=val]   | 属性值等于val    |
| Selector[attr\*=val] | 属性值包含val字符 |
| Selector[attr^=val]  | 属性值以val字符开头 |
| Selector[attr$=val]  | 属性值以val字符结尾 |

~~~css
li[type] {
  border: 1px solid gray;
}
li[type="vegetable"] {
  background-color: green;
}
li[type*=ea] {
  font-size: 100px;
}
li[color^='green'] {
  background-color: orange;
}
li[type$='t']{
  color: hotpink;
  font-weight: 900;
}

<ul>
  <li type='fruit' color='green'>西瓜</li>
  <li type='vegetable' color='greenyellow'>西兰花</li>
  <li type='meat'>牛肉</li>
  <li type='meat hot'>猪肉</li>
  <li type='drink hot'>可乐</li>
  <li type='drink hot'>雪碧</li>
  <li price='very-cheap'>红酒</li>
  <li price='very'>白酒</li>
</ul>
~~~

### 伪元素选择器

~~~css
/* .是类选择器 :是伪类选择器 ::是伪元素选择器 */
/* ::first-letter文本的第一个单词或字 */
p::first-letter {
  font-size: 20px;
  color: hotpink;
}

/* ::first-line 文本第一行 */
p::first-line {
  color: skyblue;
}

/* ::selection 可改变鼠标选中文本的样式 */
p::selection {
  /* font-size: 50px; */
  color: orange;
}

/* 在标签内部的开始和结束位置通过content属性添加元素 */
div::befor {
  content:"开始";
}
div::after {
  content:"结束";
}
~~~



# CSS 背景(background)

CSS 可以添加背景颜色和背景图片，以及来进行图片设置。
|    背景参数        |     含义    |
| ------------------------------------- | -------- |
| background-color                      | 背景颜色     |
| background-image                      | 背景图片地址   |
| background-repeat                     | 是否平铺     |
| background-attachment                 | 背景固定还是滚动 |
| background-position                   | 背景位置     |
| background:背景颜色 背景图片 背景平铺 背景滚动 背景位置| 背景的合写（复合属性）|

~~~css
div {
    /* 图片宽高 */
    width: 400px;
    height: 500px;
    
    /* 背景颜色 */
    background-color: pink;
    
    /* 背景图像 */
    background-image: url(images/l.jpg);
    
    /* 背景平铺 repeat(平铺) | no-repeat(不平铺) | repeat-x(横向平铺) | repeat-y(纵向平铺) */
    background-repeat: no-repeat;
    
    /* 背景附着 scroll(背景图像随内容滚动) | fixed(背景图像固定) */
    background-attachment: fixed;  
    
    /* 背景位置 X轴 Y轴 */
    /* 1. 使用方位名词,默认左上角 */
    background-position: left/center/right top/center/bottom;   
    /* 2. 使用精切单位 */
    background-position: 10px 30px; 
    /* 3. 混搭 */
    background-position: center 10px ;
    
    /* 背景简写 */
	background: #000 url(images/ms.jpg) no-repeat fixed center -25px;
    
    /* 背景透明 最后一个参数是alpha 透明度 取值范围 0~1 */
    background: rgba(0, 0, 0, 0.7);
    
    /* 背景缩放 会自动调整缩放比例,保证图片始终填充满背景区域*/
    background-size: cover;
    
    /* 多背景 用逗号分隔,为了避免背景色将图像盖住,背景色通常都定义在最后一组上 */
    background: url(images/l.jpg) no-repeat left top ,
			    url(images/3.jpg) no-repeat right bottom blue;
}
~~~



# CSS 三大特性

~~~css
/* 1. 层叠性：后面覆盖前面(就近原则) */
div {
    color: skyblue;
}
div {
	color: hotpink;
}

/* 2. 继承性：字标签继承父标签样式 */
div {
    color: pink;
    font-size: 20px;
}

<div>
	<p>王思聪</p>
</div>

/* 注意：继承的权重为0 */
.daohanglan {  0010是nav标签的不是li标签的，此时li标签的权重是0000
    color: red;
}
li {  0001
    color: pink;  最终文本显示pink色
}

<nav class="daohanglan">
    <ul>
    	<li>继承的权重为0</li>
    </ul>
</nav>

/* 3. 优先级：!important(∞) > 行内样式(1,0,0,0) > id选择器(0,1,0,0) > (伪)类选择器(0,0,1,0) > 标签选择器(0,0,0,1) */
div {  
    color: pink;
}
:first-child {  
    color: green;
}
.king {  
    color: blue;
}
#wang {  
    color: red;
}
div {
    color: orange!important;  /* important级别最高，一旦出现优先执行 */
}

<div class="king" id="wang" style="color: skyblue"> 王者农药 </div>

/* 优先级相同看权重叠加，如果权重都相同那就看层叠性了(就近原则) */
ul li {    0001 + 0001 = 0002
    color: green;
}
li {     0001
    color: red;
}
nav ul li {    0001 + 0001 + 0001 = 0003
    color: blue;
}
.daohang ul li {   0010 + 0001 + 0001 = 0012
    color: pink;
}

<nav class="daohang">
    <ul>
        <li>李白</li>
        <li>程咬金</li>
        <li>鲁班1号</li>
    </ul>
</nav>

~~~



# 盒子模型（重点）

CSS三大模块：  盒子模型 、 浮动 、 定位，其余的都是细节

所谓盒子模型就是把HTML页面中的元素看作是一个矩形的盒子，也就是一个盛装内容的容器。每个矩形都由元素的内容、内边距（padding）、边框（border）和外边距（margin）组成。

网页布局的本质：  把网页元素比如文字图片等等，放入盒子里面，然后利用CSS摆放盒子的过程

~~~css
.user {
    /* 盒子宽高 */
    /* 盒子的总宽度= width+左右内边距之和+左右边框宽度之和+左右外边距之和 */
    width: 300px;
    /* 盒子的总高度= height+上下内边距之和+上下边框宽度之和+上下外边距之和 */
	height: 100px;
    
    /* 1. 盒子边框 border */
    /* 边框宽度 */
    border-width: 1px;
    /* 边框样式：none(无边框) | solid(单实线) | dashed(虚线) | dotted(点线) | double(双实线) */
    border-style: solid;
    /* 边框颜色 */
    border-color: pink;
    /* 边框综合设置：四边宽度 四边样式 四边颜色 */
    border: 1px solid pink;
    /* 表格的细线边框(合并相邻边框) */
    border-collapse:collapse; 
    /* 设置圆角边框 左上角 右上角 右下角 左下角 */
    border-radius: 20px/50px;
    
    /* 2. 内边距 padding */
	/* 只写一个值表示上下左右都是10像素 */
    padding: 10px;
    /* 写四个值表示上右下左四个方向 */
    padding: 10px 20px 30px 40px;
    
    /* 3. 外边距 margin */
    /* 上下30左右auto，左右auto可以使盒子水平居中对齐 */ 
    margin: 30px auto;  
    
    /* 清除标签的默认内外边距 */
	padding: 0;
    margin: 0;
    
    /* 盒子模型布局稳定性，优先使用width */
    width > padding > margin  
    
    /* 盒子阴影box-shadow:水平位置 垂直位置 模糊距离 (阴影尺寸) 阴影颜色 */
	box-shadow: 5px 5px 3px 4px rgba(0, 0, 0, 0.4);
}
~~~



# 浮动

CSS的定位机制有3种：标准流、浮动和定位

标准流就是网页内标签元素从上到下从左到右排列顺序，比如块级元素独占一行，行内元素按顺序依次前后排列

浮动是指设置了浮动属性的元素会脱离标准普通流的控制，移动到其父元素中指定位置的过程

~~~css
div {
    width: 200px;
    height: 200px;
    background-color: pink;
    /* display: inline-block; 转换为行内块元素就可以放一行上,但是元素之间有空隙不方便处理 */
    /* 使用浮动 left | right | none  目的是让多个块元素在同一行显示 */
    float: left; 
    /* 一个父盒子里的子盒子，如果其中一个子级有浮动，则其他子级都需要浮动。这样才能一行对齐显示 */
    
    /* 清除浮动主要为了解决父级元素因为子级浮动引起内部高度为0 的问题 */
    /* 使用before和after双伪元素清除浮动 */
    .clearfix:before,.clearfix:after { 
        content:".";
        display:table;
    }
    .clearfix:after {
        clear:both;
    }
    .clearfix {
        *zoom:1;
    }
    
}
~~~



# 版心和布局流程

在制作网页时，要想使页面结构清晰、有条理，也需要对网页进行“排版”

“版心”是指网页中主体内容所在区域，一般在浏览器窗口中水平居中显示，常见的宽度值为960px、1000px

为了提高网页制作效率，需要遵守布局流程：

1、确定页面的版心（可视区）。

2、分析页面中的行模块，以及每个行模块中的列模块。

3、制作HTML页面，CSS文件。

4、CSS初始化，然后开始运用盒子模型的原理，通过DIV+CSS布局来控制网页的各个模块。

```css
/* 1. 一列固定宽度且居中 */
/* 清除内外边距 css 第一句话 */
* {
    margin: 0;
    padding: 0;  
}
/* 相同部分使用并集选择器统一设置 */
.top,.banner,.main,.footer {
    width: 960px;
    margin: 0 auto; 
    margin-bottom: 10px;
    border: 1px dashed #ccc;
}
.top {		
    height: 80px;
    background-color: pink;									
}
.banner {
    height: 120px;
    background-color: purple;
}
.main {
    height: 500px;
    background-color: hotpink;
}
.footer {
    height: 150px;
    background-color: black;
}

<div class="top">top</div>
<div class="banner">banner</div>
<div class="main">main</div>
<div class="footer">footer</div>
```

<img src="media/yl.jpg" width="400" />



```css
/* 2. 两列左窄右宽型 */
/* 清除内外边距 css 第一句话 */
* {
    margin: 0;
    padding: 0;
}
/* 相同部分使用并集选择器统一设置 */
.top,.banner,.main,.footer {
    width: 960px;
    margin: 0 auto;
    border: 1px dashed #ccc;
    text-align: center;
    background-color: #eee;
    margin-bottom: 8px;
}
.top {
    height: 80px;
}
.banner {
    height: 150px;
}
.main {
    height: 500px;
} 
.left {
    width: 360px;
    height: 500px;
    background-color: pink;
    float: left;

}
.right {
    width: 592px;
    height: 500px;
    background-color: purple;
    float: right;
}
.footer {
    height: 120px;
}

<div class="top">top</div>
<div class="banner">banner</div>
<div class="main">
    <div class="left">left</div>
    <div class="right">right</div>
</div>
<div class="footer">footer</div>
```

<img src="media/ll.jpg" width="400" />



```css
/* 3. 通栏平均分布型 */
/* 清除内外边距 css 第一句话 */
* {
    margin: 0;
    padding: 0;
}
/* 取消列表的默认样式小点 */
ul {
    list-style: none;  
}
.top {
    height: 60px;
    background-color: #000;
}
.banner {
    width: 960px;
    height: 400px;
    background-color: skyblue;
    margin: 20px auto;
    border-radius: 15px;
}
.main {
    width: 960px;
    margin: 0 auto;
    height: 200px;
}
.main ul li {
    width: 240px;
    height: 200px;
    background-color: pink;
    float: left; 
}
.main ul li:nth-child(even) {  
    background-color: purple;
}
.footer {
    height: 100px;
    background-color: #000;
}

<div class="top">top</div>
<div class="banner">banner</div>
<div class="main">
    <ul>
        <li>1</li>
        <li>2</li>
        <li>3</li>
        <li>4</li>
    </ul>
</div>
<div class="footer">footer</div>
```

<img src="media/tl.jpg" width="600" />




#定位

元素的定位属性主要包括定位模式和边偏移两部分

1、边偏移

| 边偏移属性  | 描述                      |
| ------ | ----------------------- |
| top    | 顶端偏移量，定义元素相对于其父元素上边线的距离 |
| bottom | 底部偏移量，定义元素相对于其父元素下边线的距离 |
| left   | 左侧偏移量，定义元素相对于其父元素左边线的距离 |
| right  | 右侧偏移量，定义元素相对于其父元素右边线的距离 |

定位要和边偏移搭配使用，比如 top: 100px;  left: 30px; 

2、定位模式

| 值        | 描述                       |
| -------- | ------------------------ |
| static   | 自动定位（默认定位方式）             |
| relative | 相对定位，相对于其原文档流的位置进行定位     |
| absolute | 绝对定位，相对于其上一个已经定位的父元素进行定位 |
| fixed    | 固定定位，相对于浏览器窗口进行定位        |

```css
/* 1. 静态定位：对于边偏移无效,一般用来清除定位 */
position: static;
/* 2. 相对定位：通过边偏移移动位置，但是原来的所占的位置继续占有 */
position: relative;
/* 3. 绝对定位：通过边偏移移动位置，但是完全不占位置 */
position: absolute;
/* 4. 固定定位：绝对定位的一种特殊形式 */
position: fixed;
```



# CSS界面样式

```css
/* 1. 鼠标样式 cursor：default(小白) | pointer(小手) | move(移动) | text(文本) */
<ul>
  <li style="cursor:default">我是小白</li>
  <li style="cursor:pointer">我是小手</li>
  <li style="cursor:move">我是移动</li>
  <li style="cursor:text">我是文本</li>
</ul>

/* 2. 轮廓 outline：outline-color | outline-style | outline-width */
input {
    /* 一般都取消轮廓线 */
    outline: 0;  
}

/* 3. 防止拖拽文本域 resize */
textarea {
    resize: none; 
}

/* 4. 图片和文字对齐 vertical-align: baseline(基线对齐) | top(顶部对齐) | middle(垂直居中) */
vertical-align: middle;

/* 5. 溢出文字自动换行 word-break：break-all(允许单词拆开显示) | keep-all(不允许拆开) */
word-break: break-all;

/* 6. 对象内文本显示方式 white-space：normal(默认) | nowrap(强制在同一行显示) */
white-space: nowrap;

/* 7. 文字溢出 text-overflow：clip(不显示省略标记) | ellipsis(显示省略标记) */
text-overflow: ellipsis;
```



# CSS精灵技术

为了有效减少服务器接受和发送请求的次数，提高页面的加载速度，出现了CSS精灵技术
CSS精灵是一种处理网页背景图像的方式。它将一个页面涉及到的所有零星背景图像都集中到一张大图中去，当用户访问该页面时，只需向服务器发送一次请求，网页中的背景图像即可全部展示出来

图片缺点：增加总文件的大小，增加额外"http请求"，大大降低网页性能，而且图片放大和缩小会失真
精灵技术：将小图片集中到大图片中（PC端常用）
字体图标：图标可以缩放（移动端常用）

~~~css
div {
    width: 17px;
    height: 13px;
    background: url(images/jd.png) no-repeat;
    /* 因为背景图片往上移动，所以是负值 */
    background-position: 0 -388px;  
    margin: 100px auto;
}
p {
    width: 56px;
    height: 49px;
    background: url(images/jd.png) no-repeat;
    /* 因为背景图片往上移动，所以是负值 */
    background-position: 0 -438px;  
}
~~~

# 滑动门

滑动门就是利用CSS精灵（主要是背景位置）和盒子padding撑开宽度, 以便能适应不同字数的导航栏

一般的经典布局都是这样的：

```css
* {
margin: 0;
padding: 0;
}
a {
margin: 100px;
display: inline-block;
height: 33px;
/* 千万不能给宽度 写死宽度是不对滴，我们要推拉门 自由缩放 */
background: url(images/ao.png) no-repeat;
padding-left: 15px;
color: #fff;
text-decoration: none;
line-height: 33px;
}
a span {
display: inline-block;
height: 33px;
background: url(images/ao.png) no-repeat right; 
/* span 不能给宽度 利用padding挤开  要我要span 右边的圆角  所以 背景位置 右对齐 */
padding-right: 15px;
}

<li>
  <a href="#">
    <span>导航栏内容</span>
  </a>
</li>
```

1. a 设置 背景左侧，padding撑开合适宽度。    
2. span 设置背景右侧， padding撑开合适宽度 剩下由文字继续撑开宽度。
3. 之所以a包含span就是因为 整个导航都是可以点击的。



# 过渡

过渡（transition)是CSS3中具有颠覆性的特征之一，我们可以在不使用 Flash 动画或 JavaScript 的情况下，当元素从一种样式变换为另一种样式时为元素添加效果。

帧动画：通过一帧一帧的画面按照固定顺序和速度播放。如电影胶片

在CSS3里使用transition可以实现补间动画（过渡效果），并且当前元素只要有“属性”发生变化时即存在两种状态(我们用A和B代指），就可以实现平滑的过渡，为了方便演示采用hover切换两种状态，但是并不仅仅局限于hover状态来实现过渡。

语法格式:

~~~css
div {
    width: 200px;
    height: 100px;
    background-color: pink;
    /* transition: 要过渡的属性 花费时间 运动曲线 何时开始 (多个属性之间用逗号隔开) */
    transition: width 0.6s ease 0s, height 0.3s ease-in 1s; 
    /* all表示所有的属性都变化过渡 */
    transition: all 0.6s;
}
/* 鼠标经过盒子，我们的宽度变为400 */
div:hover {  
    width: 600px;
    height: 600px;
}
~~~



## 2D变形(CSS3)

转换是CSS3中具有颠覆性的特征之一，可以实现元素的位移、旋转、变形、缩放，甚至支持矩阵方式，配合过渡和即将学习的动画知识，可以取代大量之前只能靠Flash才可以实现的效果。

变形转换 transform  

- 移动 translate(x, y) 

![1498443715586](media/1498443715586.png)

```css
translate(50px,50px);
```

使用translate方法来将文字或图像在水平方向和垂直方向上分别垂直移动50像素。

可以改变元素的位置，x、y可为负值；

~~~
 translate(x,y)水平方向和垂直方向同时移动（也就是X轴和Y轴同时移动）
 translateX(x)仅水平方向移动（X轴移动）
 translateY(Y)仅垂直方向移动（Y轴移动）
~~~

~~~css
.box {
  width: 499.9999px;
  height: 400px;
  background: pink;
  position: absolute;
  left:50%;
  top:50%;
  transform:translate(-50%,-50%);  /* 走的自己的一半 */
}
~~~

 让定位的盒子水平居中

- 缩放 scale(x, y) 

![1498444645795](media/1498444645795.png)

```css
transform:scale(0.8,1);
```

可以对元素进行水平和垂直方向的缩放。该语句使用scale方法使该元素在水平方向上缩小了20%，垂直方向上不缩放。

~~~
scale(X,Y)使元素水平方向和垂直方向同时缩放（也就是X轴和Y轴同时缩放）
scaleX(x)元素仅水平方向缩放（X轴缩放）
scaleY(y)元素仅垂直方向缩放（Y轴缩放）
~~~

 scale()的取值默认的值为1，当值设置为0.01到0.99之间的任何值，作用使一个元素缩小；而任何大于或等于1.01的值，作用是让元素放大

- 旋转 rotate(deg) 

可以对元素进行旋转，正值为顺时针，负值为逆时针；

![1498443651293](media/1498443651293.png)

~~~css
transform:rotate(45deg);
~~~

1. 当元素旋转以后，坐标轴也跟着发生的转变
2. 调整顺序可以解决，把旋转放到最后
3. 注意单位是 deg 度数

案例旋转扑克牌

~~~css
body {
  background-color: skyblue;
}
.container {
  width: 100px;
  height: 150px;
  border: 1px solid gray;
  margin: 300px auto;
  position: relative;
}
.container > img {
  display: block;
  width: 100%;
  height: 100%;
  position: absolute;
  transform-origin: top right;
  /* 添加过渡 */
  transition: all 1s;
}
.container:hover img:nth-child(1) {
  transform: rotate(60deg);
}
.container:hover img:nth-child(2) {
  transform: rotate(120deg);
}
.container:hover img:nth-child(3) {
  transform: rotate(180deg);
}
.container:hover img:nth-child(4) {
  transform: rotate(240deg);
}
.container:hover img:nth-child(5) {
  transform: rotate(300deg);
}
.container:hover img:nth-child(6) {
  transform: rotate(360deg);
}
~~~

- 倾斜 skew(deg, deg) 

![1498443827389](media/1498443827389.png)

```css
transform:skew(30deg,0deg);
```

该实例通过skew方法把元素水平方向上倾斜30度，处置方向保持不变。

可以使元素按一定的角度进行倾斜，可为负值，第二个参数不写默认为0。

5.transform-origin可以调整元素转换的原点

![1498443912530](media/1498443912530.png)

```css
 div{transform-origin: left top;transform: rotate(45deg); }  /* 改变元素原点到左上角，然后进行顺时旋转45度 */    
```

案例：  菱形照片        三角盒子  

## 3D变形

左手坐标系

伸出左手，让拇指和食指成“L”形，大拇指向右，食指向上，中指指向前方。这样我们就建立了一个左手坐标系，拇指、食指和中指分别代表X、Y、Z轴的正方向。如下图

![1498445587576](media/1498445587576.png)



CSS3中的3D坐标系与上述的3D坐标系是有一定区别的，相当于其绕着X轴旋转了180度，如下图

![1498459001951](media/1498459001951.png)

###  rotateX() 

 就是沿着 x 立体旋转.

![1498445756802](media/1498445756802.png)

~~~css
img {
  transition:all 0.5s ease 0s;
}
img:hove {

  transform:rotateX(180deg);
}
~~~

### rotateY()

沿着y轴进行旋转

![1498446043198](media/1498446043198.png)

~~~css
img {
  transition:all 0.5s ease 0s;
}
img:hove {

  transform:rotateX(180deg);
}
~~~

### rotateZ()

沿着z轴进行旋转

~~~css
img {
  transition:all .25s ease-in 0s;
}
img:hover {
  /* transform:rotateX(180deg); */
  /* transform:rotateY(180deg); */
  /* transform:rotateZ(180deg); */
  /* transform:rotateX(45deg) rotateY(180deg) rotateZ(90deg) skew(0,10deg); */
}
~~~

### 透视(perspective)

电脑显示屏是一个2D平面，图像之所以具有立体感（3D效果），其实只是一种视觉呈现，通过透视可以实现此目的。

透视可以将一个2D平面，在转换的过程当中，呈现3D效果。

注：并非任何情况下需要透视效果，根据开发需要进行设置。

perspective有两种写法

1. 作为一个属性，设置给父元素，作用于所有3D转换的子元素
2. 作为transform属性的一个值，做用于元素自身

理解透视距离原理：

![1498446715314](media/1498446715314.png)

###  开门案例

~~~css
body {
}
.door {
  width: 300px;
  height: 300px;
  margin: 100px auto;
  border: 1px solid gray;
  perspective: 1000px;
  background: url('images/dog.gif') no-repeat center/cover;
  position: relative;
}
.door > div {
  box-sizing: border-box;
  border: 1px solid black;
}
.left {
  float: left;
  width: 50%;
  height: 100%;
  background-color: brown;
  transform-origin: left center;
  transition: 1s;
  position: relative;
}
.left::before {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  top: 50%;
  right: 0px;
  transform: translateY(-10px);
  border: 1px solid whitesmoke;
}
.right {
  width: 50%;
  height: 100%;
  float: left;
  background-color: brown;
  transform-origin: right center;
  transition: 1s;
  position: relative;
}
.right::before {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  top: 50%;
  left: 0px;
  transform: translateY(-10px);
  border: 1px solid whitesmoke;
}
.door:hover .left {
  transform: rotateY(-130deg);
}
.door:hover .right {
  transform: rotateY(130deg);
}
~~~

### translateX(x)

仅水平方向移动**（X轴移动）

![1498459697576](media/1498459697576.png)

主要目的实现移动效果

### translateY(y)

仅垂直方向移动（Y轴移动）

![1498459770252](media/1498459770252.png)

### translateZ(z)

transformZ的直观表现形式就是大小变化，实质是XY平面相对于视点的远近变化（说远近就一定会说到离什么参照物远或近，在这里参照物就是perspective属性）。比如设置了perspective为200px;那么transformZ的值越接近200，就是离的越近，看上去也就越大，超过200就看不到了，因为相当于跑到后脑勺去了，我相信你正常情况下，是看不到自己的后脑勺的。

###  3D呈现（transform-style）

设置内嵌的元素在 3D 空间如何呈现，这些子元素必须为转换原素。

flat：所有子元素在 2D 平面呈现

preserve-3d：保留3D空间

3D元素构建是指某个图形是由多个元素构成的，可以给这些元素的父元素设置transform-style: preserve-3d来使其变成一个真正的3D图形。

一般而言，该声明应用在3D变换的兄弟元素们的父元素上。

### 翻转盒子案例(百度钱包)

~~~css
body {
  margin: 0;
  padding: 0;
  background-color: #B3C04C;

}

.wallet {
  width: 300px;
  height: 300px;
  margin: 50px auto;
  position: relative;
  transform-style: preserve-3d;
  transition: all 0.5s;
}

.wallet::before, .wallet::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  display: block;
  width: 100%;
  height: 100%;
  background-image: url(./images/bg.png);
  background-repeat: no-repeat;
}

.wallet::before {
  background-position: right top;
  transform: rotateY(180deg);
}

.wallet::after {
  background-position: left top;
  transform: translateZ(2px);
}

.wallet:hover {
  transform: rotateY(180deg);
}
~~~



## 动画(CSS3)

动画是CSS3中具有颠覆性的特征之一，可通过设置多个节点来精确控制一个或一组动画，常用来实现复杂的动画效果。

语法格式：

~~~css
animation:动画名称 动画时间 运动曲线  何时开始  播放次数  是否反方向;
~~~

![1498461096243](media/1498461096243.png)

关于几个值，除了名字，动画时间，延时有严格顺序要求其它随意r

~~~css
@keyframes 动画名称 {
  from{ 开始位置 }  0%
  to{  结束  }  100%
}
~~~

~~~
animation-iteration-count:infinite;  无限循环播放
animation-play-state:paused;   暂停动画"
~~~

### 小汽车案例

~~~css
body {
  background: white;
}
img {
  width: 200px;
}
.animation {
  animation-name: goback;
  animation-duration: 5s;
  animation-timing-function: ease;
  animation-iteration-count: infinite;
}
@keyframes goback {
  0%{}
  49%{
    transform: translateX(1000px);
  }
  55%{
    transform: translateX(1000px) rotateY(180deg);
  }
  95%{
    transform: translateX(0) rotateY(180deg);
  }
  100%{
    transform: translateX(0) rotateY(0deg);
  }
}
~~~

## 伸缩布局(CSS3)

CSS3在布局方面做了非常大的改进，使得我们对块级元素的布局排列变得十分灵活，适应性非常强，其强大的伸缩性，在响应式开中可以发挥极大的作用。

主轴：Flex容器的主轴主要用来配置Flex项目，默认是水平方向

侧轴：与主轴垂直的轴称作侧轴，默认是垂直方向的

方向：默认主轴从左向右，侧轴默认从上到下

主轴和侧轴并不是固定不变的，通过flex-direction可以互换。

![1498441839910](media/1498441839910.png)



Flex布局的语法规范经过几年发生了很大的变化，也给Flexbox的使用带来一定的局限性，因为语法规范版本众多，浏览器支持不一致，致使Flexbox布局使用不多

**2、各属性详解******

a、flex-direction调整主轴方向（默认为水平方向）

b、justify-content调整主轴对齐

c、align-items调整侧轴对齐

d、flex-wrap控制是否换行

e、align-content堆栈（由flex-wrap产生的独立行）对齐

f、flex-flow是flex-direction、flex-wrap的简写形式

g、flex子项目在主轴的缩放比例，不指定flex属性，则不参与伸缩分配

h、order控制子项目的排列顺序，正序方式排序，从小到大

此知识点重在理解，要明确找出主轴、侧轴、方向，各属性对应的属性值

