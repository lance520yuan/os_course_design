#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
""" 
@File    :   content    
@Contact :   18645369158@163.com  
@Modify Time      @Author    @Version    @Description
------------      -------    --------    ----------- 
2020/6/4 14:42    LanceYuan  1.0         None
"""
from code.Tree import Tree


class ContentData:
    """
    目录类，用于存放目录的数据结构及操作
    """
    def __init__(self, file_type, file_name, *args):
        """
        初始化每条目录数据
        :param file_type: 文件类型
        :param file_name: 文件名称
        :param args: 文件数据等未定参数
        """
        self.file_type = file_type
        self.file_name = file_name
        if not file_type:
            self.file_address = args[0]

    def __eq__(self, other):
        """
        重写比较函数用来判断数据重复
        :param other: 比较对象
        :return:
        """
        if self.file_name == other.filename and self.file_type == other.filetype:
            return True
        else:
            return False

    """
    用于存放目录的变量形式
    """
    file_type = int
    """
    用于存储文件类型，0为文件目录，1为文件夹
    """
    file_name = str
    """
    用于存放文件名称
    """
    file_address = str
    """
    用于存放文件的逻辑地址
    """


class Content:
    def __init__(self):
        """
        初始化目录
        """
        self.root = Tree(ContentData(0, "Lzy:"))
        """
        创建目录树
        """
        self.position = self.root
        """
        选定当前所在目录位置
        """

    def back_dir(self):
        """
        返回上级目录
        :return:
        """
        if not self.position.father:
            self.position = self.position.father

    def forward_dir(self, name):
        """
        进入目录-name
        :param name: 进入的目录名
        :return: 是否成功进入目录
        """
        exist = False
        for son in self.position.sons:
            if son.data.file_name == name:
                self.position = son
                exist = True
                break
        return exist

    def show_dir(self):
        """
        展示当前下级目录
        :return:子目录菜单
        """
        return self.position.show_sons()

    def create_dir(self, dir_name):
        """
        创建子目录
        :param dir_name: 子目录名
        :return:
        """
        new_dir = Tree(ContentData(0, dir_name), self.position)
        self.position.add_son(new_dir)

    def find_dir(self, dir_name):
        """

        :param dirname:
        :return:
        """
        pass

    def rm_dir(self, dir_name):
        """
        删除文件夹: 尚未完善，仅能从目录中移除，不能写入
        :param dir_name:
        :return: 是否存在此目录
        """
        son = self.position.find_son(ContentData(0, dir_name))
        if son:
            self.position.remove_son(son)
            return True
        else:
            return False
