#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
""" 
@File    :   explanation
@Contact :   18645369158@163.com  
@Modify Time      @Author    @Version    @Description 
------------      -------    --------    ----------- 
2020/6/1 15:35    LanceYuan  1.0         解释命令
"""
from mycode import control as C
import datetime

class Explanation:
    """
    命令解释功能
    """
    ver = "1.0"

    def the_ver(self):
        """
        静态函数，显示版本号
        :param self:
        :return:
        """
        print("Version:" + Explanation.ver)
        print("made by lanceYuan")

    def time(self):
        print(str(datetime.datetime.now()).split(".")[0])

    def __init__(self):
        """
        初始化程序
        """
        self.FCB = C.Control()
        self.command = ""
        self.command_head = "pass"
        self.command_body = ""
        self.where_now()
        self.function_dict = {
                              "cd": self.cd,
                              "dir": self.dir,
                              "mkdir": self.mkdir,
                              "rmdir": self.rmdir,
                              "touch": self.touch,
                              "write": self.write,
                              "more": self.more,
                              "ver": self.the_ver,
                              "attrib": self.attrib,
                              "del": self.del_it,
                              "copy": self.copy,
                              "xcopy": self.xcopy,
                              "help": self.help,
                              "rename": self.rename,
                              "move": self.move,
                                "time":self.time,
                                "import":self.import_it,
                                "export": self.export_it}

    def pass_one(self):
        """
        输入空格时不执行任何命令
        :return:
        """
        pass

    def where_now(self):
        """
        展示现在位置
        :return:
        """
        self.FCB.where_now()
        print(">", end="")

    def get_command(self):
        """
        获取命令并判断是否是exit，如果结果是exit则返回假
        :return: bool
        """
        self.command = input()
        if not self.command:
            self.command = "pass"
        self.command_head = self.command.split(" ")[0]
        if self.command_head == "exit":
            return False
        else:
            if len(self.command.split(" ")) > 1:
                self.command_body = self.command.split(" ", 1)[1]
            if self.command_head not in self.function_dict.keys():
                print(self.command_head+" is not recognized as an command")
            else:
                self.function_dict[self.command_head]()  # 此处self.command不可能为空故不存在问题
            self.where_now()
            return True

    def cd(self):
        """
        解析命令cd，分绝对路径相对路径进行讨论
        :return:
        """
        path = self.command_body.split('\\')
        if path[0] == "Lzy:":
            self.FCB.back_to_root()
            path.pop(0)

        for i in path:
            if i == ".":
                pass
            elif i == '..':
                self.FCB.back()
            else:
                if not self.FCB.forward(i):
                    print("The system cannot find the path specified.")

    def dir(self):
        """
        展示当前目录内容
        :return:
        """
        the_list = self.FCB.dir()
        dir_or_not = {0: "<DIR>", 1: "<FILE>"}
        file_num = 0
        file_size = 0
        if len(the_list) != 0:
            for one in the_list:
                file_num += one[1]
                file_size += one[2]
                print('%-38s' % one[0]
                      + '%-20s' % dir_or_not[one[1]]
                      + '%-20s' % (one[2] if one[2] else " ")
                      + '%-20s' % one[3])
        print("{} File(s)\n{} bytes\n{} Dir(s)".format(
            file_num,  file_size, len(the_list)-file_num))

    def mkdir(self):
        """
        创建文件夹
        :return:
        """
        if self.command_body:
            if not self.FCB.mkdir(self.command_body):
                print("A subdirectory or file os already exists.")

    def more(self):
        """
        显示输出文件
        :return:
        """
        if self.FCB.in_here(self.command_body):
            print("file below:")
            print(self.FCB.more(self.command_body))
        else:
            print("file not exist")

    def copy(self):
        """
        复制文件1到指定的目录为文件2
        :return:
        """
        cmd = self.command_body.split(" ")
        self.FCB.copy_one(cmd[0], cmd[1], cmd[2].split('.')[0])

    def rmdir(self):
        self.FCB.rmdir(self.command_body)

    def attrib(self):
        the_list = self.FCB.dir()
        dir_or_not = {0: "<DIR>", 1: "<FILE>"}
        file_num = 0
        file_size = 0
        if len(the_list) != 0:
            for one in the_list:
                if one[3] == self.command_body:
                    file_num += one[1]
                    file_size += one[2]
                    print('%-38s' % one[0]
                          + '%-20s' % dir_or_not[one[1]]
                          + '%-20s' % (one[2] if one[2] else " ")
                          + '%-20s' % one[3])
                    break

    def del_it(self):
        if self.FCB.in_here(self.command_body):
            self.FCB.delete(self.command_body)
        else:
            print("file not exist")

    def xcopy(self):
        cmd = self.command_body.split(" ")
        self.FCB.x_copy_one(cmd[0], cmd[1], cmd[2].split('.')[0])

    def rename(self):
        cmd = self.command_body.split(" ")
        if self.FCB.in_here(cmd[0]):
            self.FCB.rename(cmd[0], cmd[1])
        else:
            print("File not exist")

    def move(self):
        cmd = self.command_body.split(" ")
        self.FCB.move(cmd[0], cmd[1])

    def touch(self):
        """
        创建文件
        :return:
        """
        if len(self.command_body.split('.')) == 1:
            file_type = 'txt'
            file_name = self.command_body
        else:
            file_name = self.command_body.split('.')[0]
            file_type = self.command_body.split('.')[1]

        self.FCB.create_file(file_name, file_type)

    def write(self):
        """
        写文件内容
        :return:
        """
        if self.FCB.in_here(self.command_body):
            print("Please enter the content you want to add below, ending with :q (:q is not included in the file)")
            print("text>>",end="")
            str = ""
            endstr = ":q"
            for line in iter(input, endstr):  # 每行接收的东西
                str += line + "\n"  # 换行
            self.FCB.write_file(self.command_body, str)
        else:
            print("file not exist")

    def help(self):
        print("cmd all")
        for i in self.function_dict.keys():
            print(i)

    def import_it(self):
        outer_file = self.command_body.split(' ')[0]
        with open(outer_file, "r") as f:
            file = f.read()
        self.FCB.create_file(outer_file.split("/")[-1].split(".")[0], "txt")
        self.FCB.write_file(outer_file.split("/")[-1].split(".")[0], file)

    def export_it(self):
        if self.FCB.in_here(self.command_body.split(' ')[0]):
            with open(self.command_body.split(' ')[1]+"/"+self.command_body.split(' ')[0], "w") as f:
                f.write(self.FCB.more(self.command_body.split(' ')[0]))
        else:
            print("file not exist")

