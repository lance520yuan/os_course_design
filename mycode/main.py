#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
""" 
@File    :   main    
@Contact :   18645369158@163.com  
@Modify Time      @Author    @Version    @Description 
------------      -------    --------    ----------- 
2020/6/8 1:28   LanceYuan  1.0         None 
"""
from mycode import explanation as E

if __name__ == "__main__":
    e = E.Explanation()
    a = e.get_command()
    while a:
        a = e.get_command()