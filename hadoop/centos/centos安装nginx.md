## centos安装nginx
- 安装依赖  
yum install gcc pcre-devel zlib zlib-devel openssl openssl-devel
- 下载压缩包  
wget http://nginx.org/download/nginx-1.8.0.tar.gz
- 解压  
tar -xvf nginx-1.8.0.tar.gz
- 切换到nginx目录  
cd /usr/local/nginx-1.8.0
- 编译安装  
./configure  
make && make install  --> 安装完后/nginx/sbin目录多了nginx执行命令
- 测试配置文件  
/usr/local/nginx/sbin/nginx -t
- 启动,停止,重启  
/usr/local/nginx/sbin/nginx  
/usr/local/nginx/sbin/nginx -s stop  
/usr/local/nginx/sbin/nginx -s reload
- 浏览器访问(默认80端口)  
http://192.168.152.11
