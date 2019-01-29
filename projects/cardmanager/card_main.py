# coding=utf-8
"""
card_main: 主程序
"""

from projects.cardmanager import card_tools

# 定义无限循环,让程序自己选择何时退出
while True:

    # 显示功能菜单
    card_tools.show_menu()

    # 键盘输入
    action_str = input("请选择要执行的操作:")
    print("您选择的操作是 【%s】" % action_str)

    # 1,2,3针对名片操作(这里用in而不是int()==1 or int()==2...因为不确定用户输入的数据类型)
    if action_str in ["1", "2", "3"]:

        # 1、新增名片
        if action_str == "1":
            card_tools.new_card()

        # 2、显示全部
        if action_str == "2":
            card_tools.show_all()

        # 3、搜索名片
        if action_str == "3":
            card_tools.search_card()

    # 0退出系统
    elif action_str == "0":
        print("感谢您的使用,欢迎下次再来！")
        break  # 退出当前循环

    # 其他情况
    else:
        print("输入错误,请重新输入!")


