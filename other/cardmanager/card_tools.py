# coding=utf-8
"""
card_tools: 工具类,包含主程序要用的所有函数
"""

# 定义一个空列表存储数据,放在第一行,这样所有函数都能使用该数据
card_list = []


# 显示功能列表
def show_menu():
    print("*" * 50)
    print("欢迎使用【名片管理系统】 V 1.0")
    print("1.新增名片")
    print("2.显示全部")
    print("3.搜索名片")
    print("0.退出系统")
    print("*" * 50)


# 新增名片
def new_card():
    print("新增名片")
    print("-" * 50)

    # 1、提示用户输入名片信息
    name_str = input("请输入姓名:")
    phone_str = input("请输入电话:")
    email_str = input("请输入邮箱:")

    # 2、用字典封装这些数据
    card_dict = {
        "name": name_str,
        "phone": phone_str,
        "email": email_str
    }

    # 3、将字典添加到存储数据的列表
    card_list.append(card_dict)
    print(card_list)

    # 4、提示用户添加成功
    print("新增名片 %s 成功！" % name_str)


# 显示全部
def show_all():
    print("显示全部")
    print("-" * 50)

    # 1、先判断是否有数据,没有数据就不打印表头了
    if len(card_list) == 0:
        print("当前没有任何名片,请先添加新名片！")
        # return关键字可以返回函数的结果,也可以用来终止程序,返回到函数调用入口,return下方的语句不会被执行到
        return

    # 2、打印表头
    for name in ["姓名", "电话", "邮箱"]:
        print(name, end="\t\t")
    print("")

    # 3、打印分割线
    print("=" * 30)

    # 4、遍历循环列表
    for card_dict in card_list:
        print("%s\t\t%s\t\t%s" % (
            card_dict["name"],
            card_dict["phone"],
            card_dict["email"]
        ))


# 搜索名片
def search_card():
    print("搜索名片")
    print("-" * 50)

    # 1、提示输入信息
    find_name = input("请输入要搜索的名字:")

    # 2、遍历循环列表
    for card_dict in card_list:

        # 3、搜索到了就输出详细信息
        if card_dict["name"] == find_name:
            print("找到 %s 啦!" % find_name)
            print("姓名\t\t电话\t\t邮箱")
            print("=" * 30)
            print("%s\t\t%s\t\t%s" % (
                card_dict["name"],
                card_dict["phone"],
                card_dict["email"]
            ))

            # 4、搜索到之后进行的后续操作(尽量不要把所有代码放在一个代码块,可以调用其他函数)
            card_deal(card_dict)

            # 5、终止循环
            break

        # 没搜索到也提示一下
        else:
            print("很抱歉,没有找到 %s 同学。。。" % find_name)


# 处理搜索到的名片
def card_deal(find_dict):
    """
    :param find_dict: 搜索到的名片信息
    """

    # 输入提示
    action_str = input("请选择要继续执行的操作,[1] 修改 [2] 删除 [0] 返回上级:")

    if action_str == "1":
        # 修改名片(这里有个地方要改进,如果某个key不需要修改的话,就不用输入内容,所以这里要对用户是否输入内容做判断)

        # find_dict["name"] = input("姓名:")  # 用键盘输入重新给字典的key赋值
        # find_dict["phone"] = input("电话:")
        # find_dict["email"] = input("邮箱:")

        find_dict["name"] = input_new(find_dict["name"], "姓名:")
        find_dict["phone"] = input_new(find_dict["phone"], "电话:")
        find_dict["email"] = input_new(find_dict["email"], "邮箱:")
        print("修改名片 %s 成功！" % find_dict["name"])

    elif action_str == "2":
        # 删除名片
        card_list.remove(find_dict)
        print("删除名片 %s 成功！" % find_dict["name"])
    elif action_str == "0":
        show_menu()
    else:
        print("error input!")


# 改造input函数
def input_new(old_value, new_value):
    """
    :param old_value: 原有字典value值
    :param new_value: 用户键盘输入的新的value值
    :return: 返回结果值
    """

    # 1、提示用户输入内容
    result = input(new_value)

    # 2、判断用户是否输入了内容
    if len(result) > 0:
        # 3、如果输入内容就返回新输入的值
        return result
    else:
        # 4、如果直接回车就返回原有值
        return old_value
