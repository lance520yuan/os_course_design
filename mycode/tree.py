#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
""" 
@File    :   tree
@Contact :   18645369158@163.com  
@Modify Time      @Author    @Version    @Description
------------      -------    --------    ----------- 
2020/6/1 14:46    LanceYuan  1.0         python自建多叉树结构
"""


def class_to_dict(obj):
    """
    类转字典
    :param obj:类
    :return: 字典
    """
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        dict.update(obj.__dict__)
        return dict


class Tree:
    """
    多叉树
    """

    def __init__(self, data, father=None, *arg):
        """
        初始化树节点
        :param data:当前节点的内容
        :param father: 父节点内容
        :param arg: 子节点内容
        """
        self.file = None
        """
        如果是程序则存在file
        """
        self.data = data
        """
        当前节点信息
        """
        self.sons = []
        """
        儿子节点列表
        """
        self.father = father
        """
        父节点
        """
        for i in arg:
            self.sons.append(i)

    def __eq__(self, other):
        if self.data == other.data:
            return True
        else:
            return False

    def delete(self):
        self.file.delete()

    def add_son(self, *arg):
        """
        添加子节点
        :param arg:子节点
        :return:
        """
        for i in arg:
            self.sons.append(i)

    def remove_son(self, son):
        """
        删除子节点
        :param son: 子节点
        :return:
        """
        try:
            self.sons.remove(son)
            del son
        except ValueError:
            return False
        else:
            return True

    def show_sons(self):
        """
        返回所有子节点的值
        :return: list
        """
        return self.sons

    def find_son(self, data):
        try:
            need_son = self.sons[self.sons.index(Tree(data))]
        except ValueError:
            return None
        else:
            return need_son

    def convert_to_dict(self):
        """
        将每个节点转化为字典
        :return:
        """
        content_dict = {}
        data = class_to_dict(self.data)
        content_dict['data'] = data
        content_dict['son'] = []
        for i in self.show_sons():
            content_dict['son'].append(i.data.file_name)
        if self.father:
            content_dict['father'] = self.father.data.file_name
        else:
            content_dict['father'] = ""
        return content_dict


