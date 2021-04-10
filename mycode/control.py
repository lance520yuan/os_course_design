#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
""" 
@File    :   control
@Contact :   18645369158@163.com  
@Modify Time      @Author    @Version    @Description
------------      -------    --------    ----------- 
2020/6/1 16:34    LanceYuan  1.0         控制目录类和文件类
"""
from mycode import content as C
from mycode import file as F
import json


def save(func):
    def wrapper(self, *args, **kwargs):
        fun = func(self, *args, **kwargs)
        self.save_in_json()
        return fun

    return wrapper


class Control:
    """
    控制类
    """
    def __init__(self):
        """
        初始化控制程序
        """
        self.control = C.Content()
        self.load_the_json()

    """
    与硬件交互的存储（因为读写自文件所以物理存储模式与逻辑存储模式相同）
    """
    def save_in_json(self):
        content_dict = {'content': self.control.get_the_tree(), 'file_id': F.File.the_id}
        content_json = json.dumps(content_dict, indent=4)
        with open('disk.json', 'w') as f:
            f.write(content_json)

    def load_the_json(self):
        try:
            with open('disk.json', 'r') as f:
                conent_dict = json.loads(f.read())
            if conent_dict:
                self.control.load_the_tree(conent_dict['content'])
        except FileNotFoundError:
            pass

    def write(self):
        pass

    def read(self):
        pass

    """
    操作系统本身需求
    """
    def where_now(self):
        """
        展示现在位置
        :return:
        """
        print(self.control.where_now(), end="")

    def in_here(self, name):
        """
        查看name是否在当前目录下
        :return:
        """
        return self.control.in_here(name)

    """
    需要存储的目录操作
    """
    """
    cd 调用
    """
    @save
    def forward(self, name):
        """
        进入下级菜单name
        :param name: 下级文件夹名称
        :return:
        """
        if self.control.forward_dir(name):
            return True
        else:
            return False

    @save
    def back(self):
        """
        返回上级菜单
        :return:
        """
        self.control.back_dir()

    @save
    def back_to_root(self):
        """
        返回根路径
        :return:
        """
        self.control.to_root()

    """
    mkdir 调用
    """
    @save
    def mkdir(self, dir_name):
        """
        创建文件夹
        :param dir_name: 新建文件夹的名字
        :return:
        """
        return self.control.create_dir(dir_name)

    """
    rmdir 调用
    """
    @save
    def rmdir(self, dir_name):
        """
        移除文件夹
        :param dir_name:
        :return:
        """
        self.control.rm_dir(dir_name)

    """
    touch 调用
    """
    @save
    def create_file(self, name, file_type):
        """
        创建文件
        :param name:
        :param file_type:
        :return:
        """
        file = F.File()
        file.touch(name, file_type, "")
        self.control.create_file(name + '.' + file_type, file.name, file.size, file)

    """
    copy调用
    """
    @save
    def copy_one(self, file_name, copy_dir, copy_name):
        if not self.control.in_here(file_name):
            print("file not exist")
        content = self.more(file_name)
        position = self.control.position
        self.control.dir_to(copy_dir)
        self.create_file(copy_name, "txt")
        self.write_file(copy_name + ".txt", content)
        self.control.position = position
        return True

    """
    move 调用
    """
    @save
    def move(self, file_name, copy_dir):
        if not self.control.in_here(file_name):
            print("file not exist")
        son = self.control.get_son(file_name)
        self.control.position.sons.remove(son)
        position = self.control.position
        self.control.dir_to(copy_dir)
        self.control.position.sons.append(son)
        son.father = self.control.position
        self.control.position = position
        return True
    """
    xcopy调用
    """
    @save
    def x_copy_one(self, dir_name, copy_dir, copy_name):
        if not self.control.in_here_dir(dir_name):
            print("dir not exist")
        position = self.control.position
        self.control.dir_to(copy_dir)
        self.mkdir(copy_name)
        self.control.position = position

    """
    write 调用
    """
    @save
    def write_file(self, name, content):
        return self.control.write_file(name, content)

    """
    del 调用
    """
    @save
    def delete(self, name):
        self.control.delete(name)

    """
    不需要存储的目录操作
    """
    """
    dir 调用
    """
    def dir(self):
        """
        查看当前所在文件夹下所有文件及文件夹
        :return:
        """
        data_list = []
        for i in self.control.show_dir():
            data_list.append([i.data.file_time, i.data.file_type, i.data.file_size, i.data.file_name])
        return data_list

    """
    attrib 调用
    """
    def attrib(self):
        return self.control.position.data

    """
    more 调用
    """
    def more(self, name):
        return self.control.more(name)

    """
    rename 调用
    """
    @save
    def rename(self, before_name, after_name):
        for son in self.control.position.sons:
            if son.data.file_name == before_name:
                son.data.file_name = after_name
                print("finish")
                return True
        else:
            return False

