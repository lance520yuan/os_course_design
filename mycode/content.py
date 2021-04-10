#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
""" 
@File    :   content    
@Contact :   18645369158@163.com  
@Modify Time      @Author    @Version    @Description
------------      -------    --------    ----------- 
2020/6/1 14:42    LanceYuan  1.0         创建目录数据及目录类
"""
from mycode import tree as T
from mycode import file as F
import datetime



class ContentData:
    """
    目录类，用于存放目录的数据结构及操作
    """
    def __init__(self, *args):
        """
        初始化每条目录数据
        :param args: 文件类型、文件名称、文件地址、文件大小
        """
        if type(args[0]) == dict:
            self.file_type = args[0]['file_type']
            self.file_name = args[0]['file_name']
            self.file_time = args[0]['file_time']
            self.file_address = args[0]['file_address']
            self.file_size = args[0]['file_size']
        else:
            self.file_type = args[0]
            self.file_name = args[1]
            self.file_time = str(datetime.datetime.now()).split(".")[0]

            if args[0]:
                self.file_address = args[2]
                self.file_size = args[3]
            else:
                self.file_address = -1
                self.file_size = 0

    def __eq__(self, other):
        """
        重写比较函数用来判断数据重复
        :param other: 比较对象
        :return:
        """
        if self.file_name == other.file_name and self.file_type == other.file_type:
            return True
        else:
            return False

    def __str__(self):
        """
        输出content_data的值为name字符串
        :return:
        """
        return self.file_name

    """
    用于存放目录的变量形式
    """
    file_type = int
    """
    用于存储文件类型，0为文件目录，1为文件
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
        self.root = T.Tree(ContentData(0, "Lzy:"))
        """
        创建目录树
        """
        self.position = self.root
        """
        选定当前所在目录位置
        """

    """
    存取content目录
    """

    def get_the_tree(self):
        """
        将每个节点提取
        :return:
        """
        begin = []
        answer = []
        begin.append(self.root)
        while len(begin):
            answer.append(begin[0].convert_to_dict())
            for i in begin.pop(0).show_sons():
                begin.append(i)

        return answer

    def load_the_tree(self, content_list):
        """
        加载json目录
        :param content_list:
        :return:
        """
        content_node_list = []
        father_list = []
        son_list = []
        for i in content_list:
            content_node_list.append(
                T.Tree(ContentData(i['data'])))
            father_list.append(i['father'])
            son_list.append(i['son'])

        for i in range(len(content_node_list)):
            for j in range(len(content_node_list)):
                if father_list[i] == content_node_list[j].data.file_name:
                    content_node_list[i].father = content_node_list[j]
                    break
            for j in range(len(content_node_list)):
                for k in son_list[i]:
                    if content_node_list[j].data.file_name == k:
                        content_node_list[i].sons.append(content_node_list[j])
            if content_node_list[i].data.file_type:
                f = F.File(
                    content_node_list[i].data.file_address + "." + content_node_list[i].data.file_name.split('.')[1],
                    content_node_list[i].data.file_size)
                content_node_list[i].file = f

        self.root = content_node_list[0]
        self.position = self.root

    """
    操作系统命令
    """
    """
    判断当前位置路径
    """
    def where_now(self):
        """
        展示当前目录位置
        :return:
        """
        pointer = self.position
        now = ""
        now += pointer.data.file_name
        while pointer.father:
            pointer = pointer.father
            now = pointer.data.file_name + "\\" + now
        return now
    """
    cd 功能
    """
    def to_root(self):
        """
        返回源
        :return:
        """
        self.position = self.root

    def back_dir(self):
        """
        返回上级目录
        :return:
        """
        if self.position.father:
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

    """
    DIR 功能
    """
    def show_dir(self):
        """
        展示当前下级目录
        :return:子目录菜单
        """
        return self.position.show_sons()

    """
    mkdir 功能
    """
    def create_dir(self, dir_name):
        """
        创建子目录
        :param dir_name: 子目录名
        :return:
        """
        new_dir = T.Tree(ContentData(0, dir_name), self.position)
        datas = []
        for i in self.show_dir():
            datas.append(i.data)
        if new_dir.data not in datas:
            self.position.add_son(new_dir)
            return True
        else:
            return False

    """
    more 功能
    """
    def more(self, name):
        """
        显示内容
        :param name:
        :return:
        """
        for son in self.position.sons:
            if son.data.file_name == name:
                ft = son
                return ft.file.content

    """
    copy功能
    """
    def dir_to(self, copy_dir):
        path = copy_dir.split('\\')
        if path[0] == "Lzy:":
            self.to_root()
            path.pop(0)
        for i in path:
            if i == ".":
                pass
            elif i == '..':
                self.back_dir()
            else:
                if not self.forward_dir(i):
                    print("The system cannot find the path specified.")

    def create_file(self, file_name, file_address, file_size, file):
        """
        创建文件（仅支持下级目录创建）
        :param file_name:
        :param file_address:
        :param file_size:
        :return:
        """
        new_file = T.Tree(ContentData(1, file_name,
                                      file_address, file_size),
                          self.position)
        new_file.file = file
        datas = []
        for i in self.show_dir():
            datas.append(i.data)
        if new_file.data not in datas:
            self.position.add_son(new_file)
            return True
        else:
            return False

    def write_file(self, name, content):
        exist = False
        for son in self.position.sons:
            if son.data.file_name == name:
                ft = son
                ft.file.write(content)
                ft.data.file_size = ft.file.size
                exist = True
                break
        return exist

    def in_here(self, name):
        """
        查看文件是否在文件夹中
        :param name:
        :return:
        """
        exist = False
        for son in self.position.sons:
            if son.data.file_name == name and son.data.file_type:
                exist = True
                break
        return exist

    def in_here_dir(self, name):
        """
        查看文件是否在文件夹中
        :param name:
        :return:
        """
        exist = False
        for son in self.position.sons:
            if son.data.file_name == name and not son.data.file_type:
                exist = True
                break
        return exist

    def delete(self, name):
        for son in self.position.sons:
            if son.data.file_name == name and son.data.file_type:
                son.delete()
                self.position.sons.remove(son)

    def find_dir(self):
        """
        寻找文件及路径
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

    def get_son(self, name):
        for son in self.position.sons:
            if son.data.file_name == name:
                return son
        return None
