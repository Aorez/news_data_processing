from tkinter import *


def main():
    # 创建窗口对象的背景色
    root = Tk()

    # 创建两个列表
    list1 = ['C', 'python', 'php', 'html', 'SQL', 'java']
    list2 = ['CSS', 'jQuery', 'Bootstrap']

    # 创建两个列表组件
    listbox1 = Listbox(root)
    listbox2 = Listbox(root)

    # 第一个小部件插入数据
    for item in list1:
        listbox1.insert(0, item)

    # 第二个小部件插入数据
    for item in list2:
        listbox2.insert(0, item)

    # 将小部件放置到主窗口中
    listbox1.pack()
    listbox2.pack()
    # 进入消息循环
    root.mainloop()


if __name__ == '__main__':
    main()
