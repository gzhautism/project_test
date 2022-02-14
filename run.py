# -*- encoding=utf8 -*-
__author__ = "chengchengy"

import signal
import sys
import traceback

from Config.config import setting
from Environment.device import Device
from Environment.manager_env import generate_test_list, generate_excel_obj
from lib.Manage.executor import Scheduler
from lib.driver.core.api import *
from lib.driver.utils.logger import logger

LOGGING = logger
logger.info("开始测试")
logger.info("环境初始化")

try:
    auto_setup(__file__)
    logger.info("初始化设备监控器")
    device = Device()
except Exception as err:
    logger.error("环境初始化失败")
    sys.exit(0)
logger.info("环境初始化成功")
logger.info("读取配置文件生成用例集")
try:
    test_excel = generate_excel_obj()

    def close_excel(signum, frame):
        print("程序异常终止，关闭excel句柄")
        test_excel.save_excel()
        exit()

    signal.signal(signal.SIGINT, close_excel)   # 由Interrupt Key产生，通常是CTRL+C或者DELETE产生的中断
    signal.signal(signal.SIGTERM, close_excel)  # 请求中止进程，kill命令缺省发送
    test_list = generate_test_list(test_excel)

except Exception as err:
    print(traceback.format_exc())
    logger.error("生成用例集失败")
    logger.error(str(err))
    sys.exit(0)
if len(test_list) == 0:
    logger.error("用例集为空，请检查配置")
    sys.exit(0)
logger.info("用例集生成成功")
logger.info(str(test_list))
logger.info("开始执行用例")
results = []
success = 0
for test in test_list:
    logger.info("开始执行用例：" + str(test))
    logger.info("开始生成测试用例调度器")
    try:
        scheduler = Scheduler(test_excel, test)
        logger.info("调度器生成成功" + str(scheduler))
    except Exception:
        logger.info("调度器生成失败" + str(scheduler))
    try:
        logger.info("开始执行调度器")
        scheduler.execute()
        scheduler.test_result = "OK"
    except Exception as err:
        logger.info(str(traceback.format_exc()))
        print(traceback.format_exc())
        scheduler.test_result = "NG"
        scheduler.result_reason = str(err)
        logger.error("用例执行失败")
        logger.error(str(err))

    finally:

        logger.info("开始生成测试结果")
        scheduler.generate_task_result()
        logger.info("开始生成html测试报告")
        scheduler.generate_html_report()
        logger.info("初始化环境检查")
        if device.status:
            scheduler.check_environment()
            if scheduler.test_result != "OK":
                results.append({"name": scheduler.test_case, "result": ""})
            else:
                results.append({"name": scheduler.test_case, "result": scheduler.test_result})
                success += 1
            if test % 50 == 0:
                try:
                    logger.info("清理应用缓存")
                    scheduler.clear_cache()
                    scheduler.change_map_mode()
                except:
                    logger.error("缓存清理失败")
                    logger.info("尝试恢复设备")
                    if device.status:
                        logger.info("设备恢复成功")
                    else:
                        logger.error("环境故障,无法恢复")
                        sys.exit(0)

        else:
            logger.error("环境故障,无法恢复")
            sys.exit(0)


logger.info("任务执行完毕")
logger.info("开始生成完整报告")

details = {}

total = len(results)

details["total"] = total
details["success"] = success
details["fail"] = total - success

import jinja2, io

root = setting.path.testcase_report_path
root_dir = setting.path.testcase_resource_path + "\\template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(root_dir),
    extensions=(),
    autoescape=True
)
template = env.get_template("summary_template.html", root_dir)
html = template.render({"results": results, "detail": details})
output_file = os.path.join(root, "summary.html")
with io.open(output_file, 'w', encoding="utf-8") as f:
    f.write(html)
print(output_file)
