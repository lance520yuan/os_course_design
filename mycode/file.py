#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
""" 
@File    :   file    
@Contact :   18645369158@163.com  
@Modify Time      @Author    @Version    @Description 
------------      -------    --------    ----------- 
2020/6/1 15:16    LanceYuan  1.0         None
"""
import os


class File:
    the_id = 0

    def __init__(self, *args):
        """
        初始化
        :param args: 获取已经生产的 File the id
        """
        if args:
            self.name = args[0].split('.')[0]
            self.type = args[0].split('.')[1]
            self.size = args[1]
            self.id = File.the_id
            self.load_content()
        else:
            self.name = ""
            self.type = ""
            self.size = 0
            self.id = File.the_id
            File.the_id += 1
            self.content = ""

    def delete(self):
        os.remove("file/"+self.name + "." + self.type)

    def touch(self, name, the_file_type, content):
        """
        创建文件
        :param name: 文件命名
        :param the_file_type: 文件类型
        :param content 文件内容
        :return:
        """
        self.name = name + str(File.the_id)
        self.type = the_file_type
        self.content = content
        with open("file/"+self.name + "." + self.type, 'w') as f:
            f.write(self.content)
        self.size = os.path.getsize("file/"+self.name + "." + self.type)

    def write(self, content):
        """
        写入文件内容
        :param content:
        :return:
        """
        with open("file/"+self.name + "." + self.type, 'r') as f:
            before_content = f.read()
        with open("file/" + self.name + "." + self.type, 'w') as f:
            f.write(before_content + content)

        self.size = os.path.getsize("file/" + self.name + "." + self.type)
        self.load_content()

    def load_content(self):
        with open("file/" + self.name + "." + self.type, 'r') as f:
            self.content = f.read()
