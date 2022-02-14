# -*- encoding: utf-8 -*-
# @File    : executor.py.py
# @Contact : chengcheng@heading.loc
# @Modify Time : 2021/12/29 17:23
# @Author : chengchengy
# @Version : 1.0
# @Description : 每条用例的调度函数
from datetime import datetime

from Common.compare.compare import get_return_json, compare_data, get_return_msg
from Common.utils.files import create_folders
from Environment.manager_env import check_env_init
from lib.driver.core.helper import log
from lib.driver.report.report import LogToHtml
from lib.Manage.case_analysis import *
import json
import requests


class Scheduler(object):

    def __init__(self, excel, row, delay=0.2):
        self.excel = excel
        self.setup_col = setting.yaml["Test"]['setupIndex']
        self.teardown_col = setting.yaml["Test"]['teardownIndex']
        self.row = row
        self.test_result = False
        self.result_reason = ""
        self.delay = delay
        self.protocolId = int(self.excel.get_cell_value(self.row, 2))
        # self.inputJson = self.excel.get_cell_value(self.row, 12).split(":", maxsplit=1)[1]
        # 现在 输入的json改为 完整的json
        self.inputJson = self.excel.get_cell_value(self.row, 12)
        self.is_input = True
        if self.inputJson == '/' or self.inputJson == "\\" or self.inputJson == "":
            self.is_input = False
        self.expect_json = self.excel.get_cell_value(self.row, 14)
        self.diff = ""
        self.out_json = ""
        self.test_case = self.excel.get_cell_value(self.row, 1)
        self.response_json = ""
        # 更改执行的log目录  根据用例case num 进行创建文件夹
        self.log_path = create_folders(setting.path.cur_log_path + "\\" + str(self.test_case))
        print(self.log_path)
        self.report_path = create_folders(setting.path.testcase_report_path)
        # 设置log路径为 当前 case id的文件名路径
        set_logdir(self.log_path)

    def _setup(self):

        step_list = generate_step_list(self.excel, row=self.row, col=self.setup_col)
        if not step_list:
            return
        for s in step_list:
            if s == '/' or s == "\\" or s == "":
                return
            logger.info("操作为" + str(s))
            s = c2e(s)
            step, __id, __input = analysis_case_movement(s)
            print("step,__id,__input" + str(step) + str(__id) + str(__input))
            switch_case(self.delay).case_to_function(step)(__id, __input)

    def _teardown(self):

        step_list = generate_step_list(self.excel, row=self.row, col=self.teardown_col)
        if not step_list:
            return
        for s in step_list:
            if s == '/' or s == "\\" or s == "":
                return
            logger.info("操作为" + str(s))
            step, __id, __input = analysis_case_movement(s)
            switch_case(self.delay).case_to_function(step)(__id, __input)

    def _generate_json(self):
        if self.inputJson == '/' or self.inputJson == "\\" or self.inputJson == "":
            logger.info("json为空")
            return
        # pre_json = setting.yaml["Test"]['json']
        # pre_json["protocolId"] = self.protocolId
        logger.info("请求的protocolId为：" + str(self.protocolId))
        # self.inputJson = str(self.inputJson).replace("true","True")
        logger.info("请求的json为：" + str(self.inputJson))
        # pre_json["data"] = eval(self.inputJson)
        # self.inputJson = eval(self.inputJson)
        # logger.info("请求的json为" + str(self.inputJson))
        return self.inputJson

    def _generate_request(self):
        if not self._generate_json():
            return
        logger.info("开始请求服务器")
        url = setting.yaml["Server"]["url"] + '/pc/senddata'
        params = self._generate_json()
        logger.info("生成服务器请求参数" + str(params))

        requests.post(url, data=json.dumps({"data": params}))
        logger.info("服务器发送请求成功")

    def _acquire_json(self):
        url = setting.yaml["Server"]["url"] + '/pc/getdata'
        result = requests.get(url=url)

        logger.info("服务器result状态码:"+str(result))
        data = result
        logger.info("服务器返回值为："+str(data.text))

        logger.info("获取app数据")
        logger.info(data)
        if not data:
            return ""
        return data

    def execute(self):

        logger.info("开始执行前置动作")
        self._setup()
        snapshot("前置动作执行完成.png")
        log("前置动作执行完成", snapshot=True)
        logger.info("前置动作执行完毕")
        self._generate_request()
        logger.info("等待服务器处理数据")
        time.sleep(8)
        snapshot("已发送json数据.png")
        log("已发送json数据", snapshot=True)
        result_list = self._acquire_json()

        self.out_json = get_return_json(self.protocolId,result_list,self.is_input)

        diff = {}
        logger.info("开始差异值比对")
        try:
            self.expect_json = json.loads(self.expect_json)
        except:
            pass
        logger.info("原始值：" + str(self.expect_json))
        logger.info("原始值类型：" + str(type(self.expect_json)))
        logger.info("比对值：" + str(self.out_json))
        logger.info("比对值类型：" + str(type(self.out_json)))
        noise_data = compare_data("", self.expect_json, self.out_json, diff, 2)
        self.diff = noise_data
        self.result_reason = get_return_msg(noise_data)["msg"]

        logger.info("开始执行后置动作，还原设备")
        self._teardown()
        logger.info("后置动作执行完成")

    def _diff(self):
        pass

    def generate_task_result(self):
        logger.info("回填结果截图:"+'=HYPERLINK("' + self.log_path + '","测试图片地址")')
        self.excel.insert_value_by_index('=HYPERLINK("' + self.log_path + '","测试图片地址")', self.row, 18)
        logger.info("回填返回JSON:"+str(self.out_json))
        self.excel.insert_value_by_index(str(self.out_json), self.row, 16)
        logger.info("回填测试结果:"+str(self.test_result))
        self.excel.insert_value_by_index(self.test_result, self.row, 19)
        now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        logger.info("回填测试日期:"+now)
        self.excel.insert_value_by_index(now, self.row, 21)
        logger.info("回填预期结果:"+str(self.diff))
        self.excel.insert_value_by_index(str(self.diff), self.row, 17)
        logger.info("回填执行者:"+setting.yaml["Test"]["Author"])
        self.excel.insert_value_by_index(setting.yaml["Test"]["Author"], self.row, 20)
        logger.info("回填备注:"+self.result_reason)
        self.excel.insert_value_by_index(self.result_reason, self.row, 23)

    def generate_html_report(self):

        h = LogToHtml(script_root=self.log_path, script_name="main.py", export_dir=self.report_path,
                      test_case=self.test_case,
                      log_root=self.log_path, logfile='log.txt', lang='zh', plugins=None)
        h.report()
        pass

    def check_environment(self):
        logger.info("检查环境是否初始化成功")
        if check_env_init():
            logger.info("环境初始化成功")
            return
        logger.info("环境初始化失败")
        self._init_environment()
        return self.check_environment()

    def _init_environment(self):
        logger.info("重启应用进行初始化")
        stop_app(setting.yaml["Test"]["app"])
        time.sleep(2)
        start_app(setting.yaml["Test"]["app"])
        time.sleep(10)


"""
test_excel.insert_value_by_index('=HYPERLINK("D:\\AutoTest\\log","测试图片地址")', 2, 17)
# test_excel.cell(2,15).hyperlink("D:\AutoTest\log")
test_excel.insert_value_by_index("blocked", 2, 18)
now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
test_excel.insert_value_by_index(now, 2, 20)

test_excel.insert_value_by_index(str(diff), 2, 16)
test_excel.insert_value_by_index(__author__, 2, 19)
test_excel.insert_value_by_index("暂时只实现了json拼接，json发送和接收依赖开发工具", 2, 22)
"""

if __name__ == "__main__":
    from lib.Excel.operate_excel import Excel

    test_excel = Excel(file_path=r"D:\AutoTest\TestCase\AIDL\HMI_v1.0.5测试用例 - test.xlsx", sheet_name="自动化")
    list = generate(test_excel)
    print(list)
    for i in list:
        Scheduler(test_excel, i).execute()

    '''
    import jinja2
    results = [{"name":"AW02-JK-AIDL-0001","result":"成功"},{"name":"AW02-JK-AIDL-0002","result":"成功"},{"name":"AW02-JK-AIDL-0003","result":"成功"},{"name":"AW02-JK-AIDL-0004","result":"成功"},{"name":"AW02-JK-AIDL-0005","result":""}]
    root= r'D:\AutoTest\report\2022-01-06_17-10-30'
    root_dir= r'D:\AutoTest\resource\template'
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(root_dir),
        extensions=(),
        autoescape=True
    )
    template = env.get_template("summary_template.html",root_dir)
    html = template.render({"results": results})
    output_file = os.path.join(root, "summary.html")
    with io.open(output_file, 'w', encoding="utf-8") as f:
        f.write(html)
    print(output_file)
    '''
    pass
