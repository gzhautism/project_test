# -*- encoding: utf-8 -*-
# @File    : files.py
# @Contact : chengcheng@heading.loc
# @Modify Time : 2022/1/6 14:46
# @Author : chengchengy
# @Version : 1.0
# @Description : None

import os

"创建嵌套文件夹"


def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path
