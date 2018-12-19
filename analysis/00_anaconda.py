# coding=utf-8
"""
Python数据分析要求:
1、熟悉数据分析的流程,包括数据采集、处理、可视化等
2、掌握Python语言作为数据分析工具
3、掌握非结构化数据的处理与分析
4、掌握数据分析中常用的建模知识

Anaconda: 是一个集成了大量常用扩展包的环境,包含conda、Python等180多个科学计算包及其依赖项,并且支持所有操作系统平台;
与pip对比:
安装包: pip install xxx;conda install xxx
卸载包: pip uninstall xxx;conda uninstall xxx
升级包: pip install upgrade xxx;conda update xxx

打开Anaconda Prompt终端：
conda --version: 查看conda版本号
conda list: 查看已安装的模块列表
conda install numpy: 安装numpy库(conda install失败的话可以用pip install试下)
conda remove numpy: 卸载numpy库
anaconda search -t conda jsonpath: 寻找安装jsonpath库的资源
anaconda show timbr-io/jsonpath-rw(找到的资源,比如win-64下的某个库): 显示安装该资源的命令
conda install --channel https://conda.anaconda.org/timbr-io jsonpath-rw: 安装命令

Numpy: 科学计算库(矩阵)
Pandas: 数据分析处理库(代码库)
Matplotlib: 数据可视化库(画图)
scikit-learn: 机器学习库(算法库)
"""
