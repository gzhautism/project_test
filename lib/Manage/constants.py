# -*- encoding: utf-8 -*-
# @File    : constants.py
# @Contact : chengcheng@heading.loc
# @Modify Time : 2021/12/31 10:39
# @Author : chengchengy
# @Version : 1.0
# @Description : None


from enum import Enum


class executeType(Enum):
    error = 0
    click = 1
    swipe = 2
    check = 3
    snapshot = 4
    input = 5
    startapp = 6
    stopapp = 7
    shell = 8
    wait = 9


class checkType(Enum):
    error = 0
    id = 1
    img = 2
    text = 3


class resultType(Enum):
    error = 0
    OK = 1
    NO = 2
    NT = 3

