# -*- encoding: utf-8 -*-
# @File    : manager_env.py
# @Contact : quanl@heading.loc
# @Modify Time : 2022/1/6 11:04
# @Author : quanl
# @Version : 1.0
# @Description : None

import os.path
import time

from Config.config import setting
from lib.Excel.operate_excel import Excel
from lib.Manage.case_generate import generate
from lib.driver.core.api import exists, auto_setup
from lib.driver.core.cv import Template
from lib.driver.utils.logger import logger
from lib.poco.drivers.android.uiautomation import poco


class TestCasePath:
    @property
    def getpath(self):
        if setting.yaml["Test"]['path'] and setting.yaml["Test"]['case']:
            testcasepath = os.path.join(setting.path.testcase_root_path,
                                        setting.yaml["Test"]['path'],
                                        setting.yaml["Test"]['case'])
            if os.path.exists(testcasepath):
                return testcasepath
            raise FileNotFoundError

        else:
            raise KeyError


def generate_test_list(excel):
    protocolid = setting.yaml["Test"]['protocolid']
    exclude = setting.yaml["Test"]['exclude']
    start_row = setting.yaml["Test"]['start_row']
    if type(protocolid) != list or type(exclude) != list:
        raise "protocolid和exclude参数为空"
    return generate(excel, start_row, protocolid, exclude)

    # generate()


def generate_excel_obj():
    case_list = TestCasePath().getpath
    sheet_name = setting.yaml["Test"]["sheet_name"]
    try:
        excel = Excel(case_list, sheet_name=sheet_name)
    except Exception as err:
        logger.error("实例化excel对象失败")
        logger.error(err)
        raise
    return excel


def check_env_init():
    navigate_mode = Template(setting.path.testcase_resource_path + "\\template\\chaoqian.png")
    traffic_light = Template(setting.path.testcase_resource_path + "\\template\\开启实时路况.png")
    speech = Template(setting.path.testcase_resource_path + "\\template\\取消静音.png")
    rate = Template(setting.path.testcase_resource_path + "\\template\\比例尺.png")
    battery = Template(setting.path.testcase_resource_path + "\\template\\battery.png")

    if exists(battery,threshold=0.9) :

        for i in range(2):
            if exists(traffic_light, threshold=0.95):
                break
            poco("com.aiways.autonavi:id/iv_main_traffic_lights").click()
            time.sleep(0.5)

        for i in range(6):
            if exists(navigate_mode, threshold=0.92):
                if exists(rate, threshold=0.9):
                    break
            poco("com.aiways.autonavi:id/iv_main_refresh").click()
            time.sleep(0.5)

        for i in range(2):

            if exists(speech, threshold=0.95):
                break
            poco("com.aiways.autonavi:id/iv_main_voice").click()
            time.sleep(0.5)
        return True
    return False


if __name__ == "__main__":
    poco = AndroidUiautomationPoco(use_driver_input=True, screenshot_each_action=True)
    auto_setup(__file__)
    print(setting.path.testcase_resource_path + "\\template\\chaoqian.png")
    print(check_env_init())
