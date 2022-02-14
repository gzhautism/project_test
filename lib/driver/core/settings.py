# -*- coding: utf-8 -*-
from lib.driver.utils.resolution import cocos_min_strategy
import os
import cv2
from distutils.version import LooseVersion
from Config.config import setting


class Settings(object):
    # todo : 待修改 实现全局的变量来控制
    DEBUG = False
    LOG_DIR = setting.path.cur_log_path
    LOG_FILE = "log.txt"
    RESIZE_METHOD = staticmethod(cocos_min_strategy)
    # keypoint matching: kaze/brisk/akaze/orb, contrib: sift/surf/brief
    CVSTRATEGY = ["mstpl", "tpl", "surf", "brisk"]
    if LooseVersion(cv2.__version__) > LooseVersion('3.4.2'):
        CVSTRATEGY = ["mstpl", "tpl", "sift", "brisk"]
    KEYPOINT_MATCHING_PREDICTION = True
    THRESHOLD = setting.yaml["poco"]["THRESHOLD"]  # [0, 1]
    THRESHOLD_STRICT = setting.yaml["poco"]["THRESHOLD_STRICT"]  # dedicated parameter for assert_exists
    OPDELAY = setting.yaml["poco"]["OPDELAY"]
    FIND_TIMEOUT = setting.yaml["poco"]["FIND_TIMEOUT"]
    FIND_TIMEOUT_TMP = setting.yaml["poco"]["FIND_TIMEOUT_TMP"]
    PROJECT_ROOT = os.environ.get("PROJECT_ROOT", "")  # for ``using`` other script
    SNAPSHOT_QUALITY = setting.yaml["poco"][
        "SNAPSHOT_QUALITY"]  # 1-100 https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html#jpeg
    # Image compression size, e.g. 1200, means that the size of the screenshot does not exceed 1200*1200
    IMAGE_MAXSIZE = os.environ.get("IMAGE_MAXSIZE", None)
    SAVE_IMAGE = setting.yaml["poco"]["SAVE_IMAGE"]
