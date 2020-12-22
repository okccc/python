# coding=utf-8
import paramiko
import hdfs


def upload_ftp():
    # 获取SSHClient实例
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接SSH服务端
    # 连接SSH服务端
    client.connect("10.18.3.24", username="resourcemanager", password="OzYvOQPdQVkbrTlP")
    # 获取Transport实例
    transport = client.get_transport()
    # 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
    sftp = paramiko.SFTPClient.from_transport(transport)
    # 上传
    sftp.put("", "/upload")
    # 下载
    sftp.get("/upload/19735.txt", "./a.txt")
    # 关闭连接
    client.close()


def upload_hdfs():
    cli = hdfs.InsecureClient('sftp://resourcemanager@10.18.3.24', user='deploy')
    print(cli.list('/crm/upload'))
    cli._mkdirs('/crm/upload')
    cli.delete('/crm/aaa')
    cli.makedirs('/crm/upload')
    cli.upload('/crm/upload', '/Users/okc/modules/a.txt')


if __name__ == '__main__':
    upload_hdfs()