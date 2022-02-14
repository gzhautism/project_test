# -*- encoding=utf8 -*-
__author__ = "chengchengy"

import logging

from lib.driver.core.api import *
from lib.driver.core.helper import log
from lib.driver.utils.logger import logger

LOGGING = logger
auto_setup(__file__)
import json
from lib.Excel.operate_excel import Excel
from Common.compare.compare import compare_data
from lib.driver.report.report import LogToHtml, simple_report
from lib.poco.drivers.android.uiautomation import AndroidUiautomationPoco,poco
from Config.config import setting
poco = AndroidUiautomationPoco(use_driver_input=True, screenshot_each_action=True)

test_excel = Excel(file_path="TestCase/AIDL/HMI_v1.0.5测试用例.xlsx", sheet_name="自动化")
import datetime

protocolId = int(test_excel.get_cell_value(2, 2))

inputJson = test_excel.get_cell_value(2, 12).split(":", maxsplit=1)[1]

setup = test_excel.get_cell_value(2, 10).split("\n")

teardown = test_excel.get_cell_value(2, 11).split("\n")

print(setup)

print(teardown)

print(inputJson)

data = {"protocolId": int(protocolId), "messageType": "request", "versionName": "v_20200320", "statusCode": 0,
        "needResponse": True, "message": "", "responseCode": "", "requestCode": "", "requestAuthor": "xunfei",
        "data": eval(inputJson)}

data = json.dumps(data)

for step in setup:
    # print(step)
    action, value = step.split(":", maxsplit=1)
    # print(action,id)
    sleep(3)
    if action == "start_app":
        logger.info("打开app")
        log("打开app", snapshot=True)
        start_app(value)
        sleep(8)
    elif action == "check":
        type, id = value.split("=", maxsplit=1)
        logger.info("开始关闭实时路况")
        log("开始关闭实时路况", snapshot=True)
        result = exists(Template(r"D:\\AutoTest\\resource\\关闭实时路况.png"))
        log("实时路况关闭结果：" + str(result), snapshot=True)



    else:
        type, id = value.split("=", maxsplit=1)
        log("开始执行操作：" + type)
        poco("com.aiways.autonavi:id/iv_main_traffic_lights").click()

log("开始输入json数据" + str(data))

# outputJson = {
# "protocolId": 30000,
# "messageType": "response",
# "versionName": "v_20200320",
# "data": {
# "operaValue": 1,
# "resultCode": 10000,
# "actionType": 0,
# "operaType": 0,
# "errorMessage": ""
# },
# "statusCode": 0,
# "needResponse": False,
# "message": "",
# "responseCode": "",
# "requestCode": "",
# "requestAuthor": "xunfei"
# }


outputJson = {
    "protocolId": 30000,
    "messageType": "response",
    "versionName": "v_20200320",
    "data": {
        "operaValue": 3,
        "resultCode": 20000,
        "actionType": 0,
        "operaType": 0,
        "errorMessage": ""
    },
    "statusCode": 0,
    "needResponse": False,
    "message": "",
    "responseCode": "",
    "requestCode": "",
    "requestAuthor": "xunfei"
}

log("接收到返回的json为" + str(outputJson))

test_excel.insert_value_by_index(str(outputJson), 2, 15)
expectJson = test_excel.get_cell_value(2, 14).split(":", maxsplit=1)[1]

compare = outputJson["data"]
diff = {}
diff = compare_data("", eval(expectJson), compare, diff, 2)
log("预期与实际对比的差异为 :" + str(diff))

for step in teardown:
    # print(step)
    action, value = step.split(":", maxsplit=1)
    print(action, id)
    sleep(3)
    if action == 'stop_app':
        log("关闭app", snapshot=True)
        stop_app(value)
    elif action == "check":
        type, id = value.split("=", maxsplit=1)
        log("检查实时路况", snapshot=True)
        result = exists(Template(r"D:\\AutoTest\\resource\\关闭实时路况.png"))
        log("实时路况关闭结果：" + str(result), snapshot=True)


    else:
        type, id = value.split("=", maxsplit=1)
        log("开始执行操作：" + action)
        poco("com.aiways.autonavi:id/iv_main_traffic_lights").click()

log("用例执行结束")

test_excel.insert_value_by_index('=HYPERLINK("D:\\AutoTest\\log","测试图片地址")', 2, 17)
# test_excel.cell(2,15).hyperlink("D:\AutoTest\log")
test_excel.insert_value_by_index("blocked", 2, 18)
now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
test_excel.insert_value_by_index(now, 2, 20)

test_excel.insert_value_by_index(str(diff), 2, 16)
test_excel.insert_value_by_index(__author__, 2, 19)
test_excel.insert_value_by_index("暂时只实现了json拼接，json发送和接收依赖开发工具", 2, 22)
h = LogToHtml(script_root=setting.path.cur_log_path, script_name="main.py", export_dir="D:\\AutoTest\\report",
              log_root=setting.path.cur_log_path, logfile='log.txt', lang='zh', plugins=None)
h.report()

