# coding: utf-8
import imaplib
import email
from email.header import decode_header


def get_pdf():
    """
    python imaplib自动下载邮件附件
    参考文档：http://www.pythoner.com/414.html
            http://pythonfans.lofter.com/post/3dd906_154c5c2
    """

    # 连接imap4服务器
    con = imaplib.IMAP4_SSL("imap.exmail.qq.com", 993)
    # print(type(con))  # <class 'imaplib.IMAP4_SSL'>
    # 用户登录邮箱
    con.login("info-receiver@meihaofenqi.com", "Info1234")
    # 选定一个邮件文件夹(默认是INBOX收件箱),可用con.list()查看都有哪些文件夹
    con.select()
    # 查询选定文件夹下的邮件,返回邮件编号
    # typ, mails = con.search(None, 'ALL')  # 读取所有邮件
    typ, mails = con.search(None, 'UNSEEN')  # 读取未读邮件
    # print(mails)  # [b'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20']
    # print(type(mails[0]))  # <class 'bytes'>

    # 存放附件目录
    path = "./pdf/"

    # 遍历所有邮件
    for i in mails[0].split():
        # 使用RFC822协议获取指定编号的邮件内容
        typ, data = con.fetch(i, '(RFC822)')
        # print(type(data))  # <class 'list'>

        # 获取字节数据
        mail_body = data[0][1]
        # print(type(mail_body))  # <class 'bytes'>

        # 解析bytes获取邮件信息
        mail = email.message_from_bytes(mail_body)
        # print(type(mail))  # <class 'email.message.Message'>
        # print(type(mail.walk()))  # <class 'generator'>

        # 将该邮件标记为已读
        con.store(i, '+FLAGS', '\\SEEN')

        # 获取附件
        for part in mail.walk():
            # print(type(part))  # <class 'email.message.Message'>

            # is_multipart()为true都不是附件
            if not part.is_multipart():
                # 获取附件名称
                filename = part.get_filename()
                # 获取附件内容
                content = part.get_payload(decode=True)

                # 对附件名解码(若为纯数字/字母就不需要解码)

                # print(decode_header(filename))  # [(b'\xca\xd5\xd6\xa7\xc3\xf7\xcf\xb8\xd6\xa4\xc3\xf7_2018051200085001202425326363360012577001.pdf', 'gb18030')]
                # filename_tmp = decode_header(filename)[0][0]
                # print(filename_tmp)  # b'\xca\xd5\xd6\xa7\xc3\xf7\xcf\xb8\xd6\xa4\xc3\xf7_2018051200085001202425326363360012577001.pdf'
                # charset = decode_header(filename)[0][1]
                # print(charset)  # gb18030
                # filename = filename_tmp.decode(charset)
                # print(filename)  # 收支明细证明_2018051200085001202425326363360012577001.pdf

                if filename:
                    filename = decode_header(filename)[0][0].decode(decode_header(filename)[0][1])
                    print(filename)  # 收支明细证明_2018052000085001022968455540540094637771.pdf

                    if filename.startswith("收支明细证明"):
                        # 保存附件(往文件写二进制数据要用wb模式)
                        with open(path + filename, "wb") as f:
                            # 写入文件
                            f.write(content)
    # 关闭当前选中的邮箱
    con.close()
    # 退出服务器连接
    con.logout()


if __name__ == "__main__":
    get_pdf()