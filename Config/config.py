# -*- encoding: utf-8 -*-
# @File    : test.py
# @Contact : chengcheng@heading.loc
# @Modify Time : 2021/12/28 17:48
# @Author : chengchengy
# @Version : 1.0
# @description ： 包含了一些简单的配置项，主要是框架的设置
#                 调用方法 导入setting实例就可以使用


import yaml
import os
import time


# 返回yaml解析结果的类
class Yaml:
    # 解析yaml数据

    path = None

    def __init__(self, path=None) -> None:
        Yaml.path = path

    @classmethod
    def pyaml(cls):
        # yaml 格式读取 utf8 和“ISO-8859-1”两种编码方式
        with open(cls.path, "r", encoding="utf-8") as f:
            try:
                cfg = f.read()
            except:
                with open(cls.path, "r", encoding="ISO-8859-1") as f:
                    cfg = f.read()
        return yaml.load(cfg, Loader=yaml.FullLoader)


# 解析所有路径相关的 路径类
class Path:
    # 配置项 config 路径
    config_path = os.path.abspath(os.path.dirname(__file__))
    # 项目根路径
    root_path = os.path.abspath(os.path.dirname(config_path) + os.path.sep + ".")
    # log 根路径
    log_root_path = os.path.abspath(root_path + "\\log")
    # log 文件夹名称
    log_folder_name = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    # 最新的执行log的完整路径
    cur_log_path = os.path.abspath(log_root_path + "\\" + log_folder_name)
    # 测试用例的根目录
    testcase_root_path = os.path.abspath(root_path + "\\" + "TestCase")
    # 测试过程中的图片临时存放路径
    testcase_img_path = os.path.abspath(cur_log_path + "\\" + "test_pic")
    # 测试资源图片存放路径
    testcase_resource_path = os.path.abspath(root_path + "\\" + "resource")
    # 测试报告图片路径
    testcase_report_path = os.path.abspath(root_path + "\\" + "report\\"+log_folder_name)


# 所有设置的总类
class Setting:
    """
        使用方法： 导入setting实例 setting.log setting.yaml
                返回为参数字典
    """

    @property
    def yaml(self):
        path = os.path.split(os.path.realpath(__file__))[0]
        return Yaml(path + "\\setting.yaml").pyaml()

    @property
    def path(self):
        return Path


setting = Setting()

if __name__ == "__main__":
    print(setting.yaml["Test"]['case'])
    print(setting.path.testcase_root_path)
    url = setting.yaml["Server"]["url"] + '/pc/senddata'

    print(url)

