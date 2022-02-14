# -*- encoding: utf-8 -*-
# @File    : device.py
# @Contact : zuhe@heading.loc
# @Modify Time : 2022/1/5 11:04
# @Author : zuheg
# @Version : 1.0
# @Description : None
import subprocess
import os
import sys
import time
import traceback
import timeout_decorator
import PIL.Image
import adbutils
from Config.config import setting
from lib.driver.utils.logger import logger


class Device(object):
    def __init__(self):
            pass

    @property
    def status(self):
        return self.check_status() and self.check()


    def start_app(self):
        """重启app"""
        os.system("adb shell pm clear com.aiways.autonavi")
        os.system("adb shell am start -W -n com.aiways.autonavi/com.aiways.autonavi.activity.StartupActivity")

    def monitor_app(self):
        """监控APP进程状态及cpu利用率"""
        try:
            app_cmd = 'adb shell "top -n 10 -d 1|grep com.aiways.autonavi"'
            proc = subprocess.Popen(app_cmd,
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
            try:
                top_values = proc.communicate()[0].decode().replace("\r", "").split("\n")[:-1]
            except KeyboardInterrupt:
                print("终止app状态监控服务，默认返回True")
                return True
            cpu_uz = []
            state_uz = []
            for item in top_values:
                stdout_value = item.replace("  ", " ").replace("   ", " ").split(" ")
                app_details = [x.strip() for x in stdout_value if x.strip() != ""]
                cpu_value = app_details[8]
                state_value = app_details[7]
                if float(cpu_value) > 70:
                    cpu_uz.append(cpu_value)
                if state_value == "D":
                    state_uz.append(state_value)
            if len(cpu_uz) > 9 and len(state_uz) > 0:
                print("app卡死，准备重启中！")
                start_time = time.time()
                self.start_app()
                stop_time = time.time()
                print(f"app已重启,用时{'%.2f' % (stop_time - start_time)}秒,请重新测试!")
                return False
            else:
                return True
        except ValueError as err:
            print("ValueError: %s" % err)
            return None, None
        except IOError as err:
            print("IOError: %s" % err)
            return None, None

    @timeout_decorator.timeout(15)
    def reboot(self):
        """重启设备"""
        os.system("adb reboot")
        while True:
            serial_list = [d.serial for d in adbutils.adb.device_list()]
            if serial_list:
                break
            time.sleep(1)

    def adb_server(self):
        """adb重启"""
        os.system("adb kill-server")
        time.sleep(2)
        os.system("adb start-server")

    def check_status(self):
        """获取、更新当前设备状态"""
        try:
            serial_list = [d.serial for d in adbutils.adb.device_list()]
        except KeyboardInterrupt:
            logger.info("终止获取当前设备状态操作,默认为False")
            return False
        if serial_list:
            return True
        else:
            count = 0
            vl_list = []
            while count < 3:
                count += 1
                try:
                    self.adb_server()
                    self.reboot()
                except KeyboardInterrupt:
                    print("终止设备重启!默认为False")
                    break
                except Exception as err:
                    print("设备重启超时，请检测")
                    logger.error(str(err))
                    print(traceback.format_exc())
                    #sys.exit(0)
                serial_two = [item.serial for item in adbutils.adb.device_list()]
                if serial_two:
                    vl_list.append("True")
                    break
                else:
                    vl_list.append("False")
                    continue
            if "True" in vl_list:
                return True
            else:
                return False

    def screenshot(self):
        """截取异常图片"""
        try:
            img_path = os.mkdir(setting.path.testcase_resource_path+"\\error")
            os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
            os.system("adb pull /sdcard/screenshot.png %s" % img_path)
        except:
            os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
            os.system("adb pull /sdcard/screenshot.png %s" % (setting.path.testcase_resource_path+"\\error"))
        return setting.path.testcase_resource_path+"\\error"+"\\screenshot.png"

    def check(self):
        import cv2
        import numpy
        import PIL
        # 把图片转换为单通道的灰度图
        img = self.screenshot()
        #img = r"D:\AutoTest\resource\error\飞书20220119-102835.png"
        image = PIL.Image.open(img)
        image_data = numpy.asarray(image)
        gray_img = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
        # 获取灰度图矩阵的行数和列数
        r, c = gray_img.shape[:2]
        piexs_sum = r * c  # 整个弧度图的像素个数为r*c
        # 获取偏暗的像素(表示0~19的灰度值为暗) 此处阈值可以修改
        dark_points = (gray_img < 20)
        target_array = gray_img[dark_points]
        dark_sum = target_array.size
        # 判断灰度值为暗的百分比
        dark_prop = dark_sum / (piexs_sum)
        print(dark_prop)
        if dark_prop >= 0.75:
            print("黑色图")
            return False
        return True


if __name__ == '__main__':
    q = time.time()
    d = Device()
    # d.screenshot()
    print(d.status)
    w = time.time()
    print(f"用时:{'%.4f' % (w - q)}")
