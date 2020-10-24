## centos安装python3
[参考文档](http://www.cnblogs.com/JahanGu/p/7452527.html)
```bash
# 查看已有版本和安装路径
python -V && which python
# 安装依赖  
yum install zlib-devel openssl-devel libffi-devel
# 官网下载python3  
wget https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tar.xz  
# 解压  
tar -xvf Python-3.7.5.tar.xz
# 进入python目录  
cd Python-3.7.5
# 编译安装  
./configure prefix=/usr/local/python3  
make && make install  # 安装完发现/usr/local目录下已经有python3
# 添加软链接到执行目录/usr/bin  
ln -s /usr/local/python3/bin/python3 /usr/bin/python
# python3自带pip3给pip添加软连接,以后pip安装的包都在/usr/local/python3/lib/python3.6/site-packages目录下,可以添加软连接
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip
# 由于CentOS7自带的yum采用的是python2.7,所以要指定python2作为yum的解释器  
vim /usr/bin/yum  
#! /usr/bin/python --> #! /usr/bin/python2
# 使用yum安装工具包时报错File "/usr/libexec/urlgrabber-ext-down", line 28 解决方法同上
vim /usr/libexec/urlgrabber-ext-down
#! /usr/bin/python --> #! /usr/bin/python2

# pip常用命令  
安装：pip install requests  
卸载：pip uninstall requests  
升级：pip install --upgrade requests  
搜索包：pip search requests  
查看所有包：pip list/freeze  
查看可升级包：pip list -o  
导出所有包：pip freeze > requirements.txt & pip install -r requirements.txt  
查看包详细信息：pip show requests  

$ pip show requests
Name: requests
Version: 2.21.0
Summary: Python HTTP for Humans.
Home-page: http://python-requests.org
Author: Kenneth Reitz
Author-email: me@kennethreitz.org
License: Apache 2.0
Location: c:\users\admin\appdata\roaming\python\python36\site-packages
Requires: certifi, idna, chardet, urllib3
Required-by: moviepy, itchat, baidu-aip
```  

### python3安装virtualenv
[参考文档](https://www.zhuxiongxian.cc/2017/09/28/python-install-virtualenv-and-virtualenvwrapper/)
- <font color=red>不同项目使用的包版本可能不一样,最好每个项目单独使用一个虚拟环境,是真实python环境的复制版本</font>

- 安装virtualenv  
pip install virtualenv
- 可能会碰到以下错误  
pip._vendor.urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out.  
解决：将报错的域名添加到信任列表 pip install --trusted-host files.pythonhosted.org virtualenv
- 安装virtualenvwrapper  
pip install virtualenvwrapper
- 将virtualenvwrapper.sh配入当前shell环境  
![](images/virtualenv配置.png)
- 使环境变量生效  
source ~/.bash_profile
- 添加软连接  
ln -s /usr/local/python3/bin/virtualenv /usr/bin/virtualenv
- 查看是否可用  
mkvirtualenv --help
- 常用命令  
创建：mkvirtualenv test  
删除：rmvirtualenv test  
进入：workon test  
退出：deactivate  
查看所有：lsvirtualenv
- 安装django  
pip install django==1.8.2
- 查看版本  
![](images/查看django版本.png)
- python项目一键导入所有安装包  
将当前环境依赖包生成到文件：pip freeze > requirements.txt  
在新环境安装文件中的所有包：pip install -r requirements.txt