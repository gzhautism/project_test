# -*- encoding: utf-8 -*-
# @File    : symbol_translate.py
# @Contact : chengcheng@heading.loc
# @Modify Time : 2021/12/31 13:42
# @Author : chengchengy
# @Version : 1.0
# @Description : 将字符串中的中文符号转化成英文符号


def c2e(value):
    """
    @param value: 需要转化的字符串
    @return:  转化成英文字符串
    """
    table = {ord(f): ord(t) for f, t in zip(
        u'：，￥。！？【】（）％＃＠＆１２３４５６７８９０',
        u':,$.!?[]()%#@&1234567890')}

    return value.translate(table)

def e2c(value):
    """
    @param value: 需要转化的字符串
    @return: 转化成中文字符串
    """
    table = {ord(t): ord(f) for f, t in zip(
        u'，￥。！？【】（）％＃＠＆１２３４５６７８９０',
        u',$.!?[]()%#@&1234567890')}

    return value.translate(table)
