#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
""" 
@File    :   Tree    
@Contact :   18645369158@163.com  
@Modify Time      @Author    @Version    @Description
------------      -------    --------    ----------- 
2020/6/4 14:46    LanceYuan  1.0         python自建多叉树结构
"""


class Tree:
    def __init__(self, data, father=None, *arg):
        """
        初始化树节点
        :param data:当前节点的内容
        :param father: 父节点内容
        :param arg: 子节点内容
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
            need_son = self.sons[self.sons.index(data)]
        except ValueError:
            return None
        else:
            return need_son
