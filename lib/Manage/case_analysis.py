# -*- encoding: utf-8 -*-
# @File    : case_analysis.py
# @Contact : chengcheng@heading.loc
# @Modify Time : 2021/12/31 10:50
# @Author : chengchengy
# @Version : 1.0
# @Description : 用例解析模块
from Config.config import setting
from lib.Excel.operate_excel import Excel
from lib.driver.utils.logger import logger
from lib.Manage.constants import executeType, checkType
from lib.poco.drivers.android.uiautomation import poco
from Common.utils.symbol_translate import c2e
from lib.driver.core.api import *
import os


class switch_case(object):
    def __init__(self, delay=4):
        self.delay = delay

    def case_to_function(self, case):
        fun_name = "case_type_" + str(case)
        logger.info("执行的操作函数为："+fun_name)
        method = getattr(self, fun_name, self.case_type_other)
        return method

    def case_type_1(self, _id, _input=None):
        """
        @param _input: 输入模式时的内容
        @param _id:  需要执行的  id号码
        @return:CLICK
        """
        logger.info("执行click操作："+str(_id)+str(_input))
        _id = _id.strip('"')
        if _id.startswith("text"):
            logger.info("text:"+_id.split("=")[1].strip().strip('"').strip("'"))
            poco(text=_id.split("=")[1].strip().strip('"').strip("'")).wait_for_appearance(timeout=10)
            poco(text=_id.split("=")[1].strip().strip('"').strip("'")).click()
        elif _id.startswith("img"):
            logger.info("img: "+setting.path.testcase_resource_path+"\\template\\"+_id.split("=")[1].strip().strip('"').strip("'"))
            touch(Template(setting.path.testcase_resource_path+"\\template\\"+_id.split("=")[1].strip().strip('"').strip("'")))
        else:
            if not _input:
                poco(_id).wait_for_appearance(timeout=10)
                poco(_id).click()
            else:
                _input = _input[1].strip("'").strip('"')
                poco(_id).wait_for_appearance(timeout=10)
                poco(_id)[int(_input)-1].click()
        time.sleep(self.delay)

    def case_type_2(self, _id, _input=None):
        coord = eval(_id)
        print(coord)
        logger.info("执行滑动操作:"+str(coord))
        x1, y1, x2, y2, times = coord
        if x1 < 1 and y1 < 1:
            w, h = poco.get_screen_size()
            x1 = x1 * w
            y1 = y1 * h
            x2 = x2 * w
            y2 = y2 * h
        print(x1, y1, x2, y2)
        for i in range(times):
            swipe((x1, y1), (x2, y2))
            time.sleep(2)
        time.sleep(self.delay)

    def case_type_3(self, _id, _input=None):
        """
        @param _id:
        @param _input:
        @return: CHECK
        """
        logger.info("执行检查命令："+str(_id)+str(_input))
        if _id.startswith(checkType.text.name):
            text = _id.split("=")[1].strip().strip('"')
            return str(poco(text=text.strip('"')).attr(_input[0])).lower() == _input[1]
        elif _id.startswith(checkType.img.name):
            print(setting.path.testcase_resource_path + "\\" + _id.split("=")[1].strip().strip('"'))
            return exists(Template(setting.path.testcase_resource_path + "\\" + _id.split("=")[1].strip().strip('"')))
        time.sleep(self.delay)

    def case_type_4(self, _id, _input=None):
        """
        @param _id:
        @param _input:
        @return: 截图
        """
        logger.info("执行截图命令，图片名称为："+str(_id.strip('"').strip("")))
        snapshot(_id.strip("'").strip("'") + ".png")
        time.sleep(self.delay)

    def case_type_5(self, _id, _input=None):
        """
        @param _id:  需要输入的id文本框
        @param _input: 输入的内容
        @return: 输入文本
        """
        #poco(_id).click()
        sleep(1)
        logger.info("输入文本为："+str(_input[1].strip('"')))
        # text(_input[1].strip('"'))
        poco(_id).set_text(_input[1].strip('"'))
        time.sleep(self.delay)

    def case_type_6(self, _id, _input=None):
        logger.info("执行start_app命令：" + str(_id))
        start_app(_id)
        time.sleep(self.delay)

    def case_type_7(self, _id, _input=None):
        logger.info("执行stop_app命令：" + str(_id))
        stop_app(_id)
        time.sleep(self.delay)

    def case_type_8(self, _id, _input=None):
        logger.info("执行shell命令："+str(_id))
        shell(_id)
        time.sleep(self.delay)

    def case_type_9(self, _id, _input=None):
        logger.info("执行等待命令："+str(_id))
        time.sleep(int(_id))
        time.sleep(self.delay)

    def case_type_other(self):
        logger.error("不存在当前操作方法")
        raise


"""
    error = 0
    click = 1
    swipe = 2
    check = 3
    snapshot = 4
    input = 5
    start_app = 6
    stop_app = 7


"""


def generate_step_list(excel, row, col=10):

    step_list = excel.get_cell_value(row, col)
    if not step_list:
        return ""
    step_list = step_list.split("\n")
    step_list = [i for i in step_list if i != '']
    logger.info("测试执行步骤为：" + str(step_list))
    return step_list


def analysis_case_movement(line):
    """
    @param excel:  传入的excel每行的关键字
    @return:
    """
    if not line:
        return

    action, value = line.split(":", maxsplit=1)
    action = action.strip()
    value = value.strip()
    logger.info("action,value:" + str(action) + "," + str(value))

    if action not in executeType.__members__:
        logger.error(str(action) + " : 不是执行关键字，请确认")
        raise
    step = 0
    if action == executeType.click.name:
        logger.info("执行点击操作")
        step = executeType.click.value
    elif action == executeType.swipe.name:
        logger.info("执行滑动操作")
        step = executeType.swipe.value
    elif action == executeType.check.name:
        logger.info("执行检查操作")
        step = executeType.check.value
    elif action == executeType.snapshot.name:
        logger.info("执行截图操作")
        step = executeType.snapshot.value
    elif action == executeType.input.name:
        logger.info("执行输入操作")
        step = executeType.input.value
    elif action == executeType.startapp.name:
        logger.info("执行打开app操作")
        step = executeType.startapp.value
    elif action == executeType.stopapp.name:
        logger.info("执行关闭app操作")
        step = executeType.stopapp.value
    elif action == executeType.shell.name:
        step = executeType.shell.value
    elif action == executeType.wait.name:
        logger.info("执行等待操作")
        step = executeType.wait.value
    __id, __input = _analysis_step(value)
    return step, __id, __input


'"id=sdsadsadsad,value="dsadsads"'
"sdsadsa"
""
'"sdsadsadsad,value="dsadsads"'


def _analysis_step(value):
    value = c2e(value)
    logger.info(value)
    __input = ""
    if "," in value and value.count(",") == 1:
        if not value.split(",")[0].startswith("Id"):
            __id = value.split(",")[0]
            __input = value.split(",")[1].split("=")
        else:
            __id = value.split(",")[0].split("=")[1]
            __input = value.split(",")[1].split("=")

    else:
        if value.startswith("id"):
            __id = value.split("=")[1]
        else:
            __id = value

    __id = __id.strip().strip('"').strip("'")
    logger.info("__id,__input")
    logger.info(str(__id) + str(__input))
    return __id, __input


def _executre(step, _Id, _input):
    if step not in executeType._value2member_map_:
        logger.error("测试的步骤不存在，请检查" + str(step))
        raise

    if step == executeType.error.value:
        logger.error("步骤类型错误，请检查" + str(step))


def _normalize(value):
    if "=" in value:
        value.split("=", maxsplit=1)
    pass


if __name__ == "__main__":
    _ = 'click:text="大路优先"'
    step, __id, __input = analysis_case_movement(_)
    print(step, __id, __input)
    time.sleep(8)
    switch_case().case_to_function(step)(__id, __input)
