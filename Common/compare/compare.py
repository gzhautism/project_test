# -*- encoding: utf-8 -*-
# @File    : test.py
# @Contact : chengcheng@heading.loc
# @Modify Time : 2021/12/28 17:48
# @Author : chengchengy
# @Version : 1.0
# @Description : 比对数据
import json
resultcode_msg = {
    10000: "请求成功",
    10001: "非法参数",
    10002: "缺少离线地图数据",
    10003: "地图软件未授权",
    10004: "未规划路线",
    10005: "未设置家",
    10006: "未设置公司",
    10007: "比例尺已最大",
    10008: "比例尺已最小",
    10009: "网络不畅",
    10010: "不支持的视图",
    10011: "途经点重复",
    10012: "途经点已满",
    10013: "起点错误",
    10014: "终点错误",
    10015: "途经点错误",
    10016: "路线规划失败",
    10018: "导航未启动",
    10019: "无网无数据",
    10020: "未知错误",
    10021: "城市不支持",
    10022: "道路不支持",
    10023: "未找到结果",
    10024: "无权限访问",
    10025: "引擎初始化失败",
    10026: "SDK初始化错误",
    10027: "Auto未启动",
    10028: "功能不支持",
    10029: "后台下不支持",
    10030: "回调异常",
    10031: "监听为空",
    10032: "请求失败",
    10033: "连接失败",
    10034: "执行动作取消",
    10035: "设置家成功",
    10036: "设置公司成功",
    10037: "设置普通收藏点成功",
    10038: "当前已静音",
    10039: "当前已恢复静音",
    10040: "当前已在全览模式",
    10041: "请求频繁，请稍后重试",
    10042: "路线刷新失败，请稍后重试",
    10043: "没有停车场数据",
    10044: "正在响应缩放比例尺",
    10045: "开启避开限行失败，未设置车牌号",
    10046: "重复设置偏好"
}


def compare_data(set_key, src_data, dst_data, noise_data, num):
    if isinstance(src_data, dict) and isinstance(dst_data, dict):
        """若为dict格式"""
        for key in dst_data:
            if key not in src_data:
                print("src不存在这个key")
                noise_data[key] = "src不存在这个key"
        for key in src_data:
            if key in dst_data:
                if src_data[key] != dst_data[key] and num == 1:
                    noise_data[key] = "容忍不等"
                if src_data[key] != dst_data[key] and num == 2:
                    noise_data[key] = {}
                    noise_data[key]["预期"] = src_data[key]
                    noise_data[key]["实际"] = dst_data[key]
                """递归"""
                compare_data(key, src_data[key], dst_data[key], noise_data, num)
            else:
                noise_data[key] = ["dst不存在这个key"]
    elif isinstance(src_data, list) and isinstance(dst_data, list):
        """若为list格式"""
        if len(src_data) != len(dst_data) and len(set_key) != 0:
            print("_list len: '{}' != '{}'".format(len(src_data), len(dst_data)))
            noise_data[set_key]["预期"] = str(src_data)
            noise_data[set_key]["实际"] = str(dst_data)
            return
        if len(src_data) == len(dst_data) and len(src_data) > 1:
            for index in range(len(src_data)):
                for src_list, dst_list in zip(sorted(src_data[index]), sorted(dst_data[index])):
                    """递归"""
                    compare_data("", src_list, dst_list, noise_data, num)
        else:
            for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
                """递归"""
                compare_data("", src_list, dst_list, noise_data, num)
    else:
        if str(src_data) != str(dst_data):
            print("src_data", src_data, "dst_data", dst_data)
    return noise_data


def get_return_msg(noise_data):
    code = {"returnCode": 10000, "msg": "请求成功"}
    if "resultCode" in noise_data:
        code_msg = noise_data.get("resultCode", None)
        if isinstance(code_msg, list):
            code['msg'] = code_msg[0]
        else:
            msg = resultcode_msg.get(code_msg.get("实际", {}))
            code['returnCode'] = code_msg.get("实际", {})
            code['msg'] = msg
    return code


def get_return_json(id, data, is_input):
    data_aa = json.loads(data.text).get('data', [])
    json_data = {}
    special_id = ['80089', "30008"]
    data_aa.reverse()
    for i in data_aa:
        if is_input and str(id) not in special_id and str(id) == str(i.get("protocolId", "")) \
                and i.get("messageType", '') == "response":
            json_data = i
            break
        elif i.get("messageType", '') == "dispatch":
            if str(id) == "30008" and str(i.get("protocolId", "")) == "30200":
                json_data = i
                break
            elif str(id) == str(i.get("protocolId", "")):
                json_data = i
                break
    return json_data


if __name__ == "__main__":
    dict1 = {
 "protocolId": 30402,
 "messageType": "response",
 "versionName": "v_20200320",
 "data": {
 "midPoiArray": "",
 "midPoisNum": 0,
 "count": 0,
 "fromPoiName": "",
 "toPoiLongitude": 0.01,
 "toPoiName": "",
 "toPoiLatitude": 0.01,
 "protocolRouteInfos": [
 {
 "protocolCityInfos": [
 {
 "viaCityName": ""
 }
 ],
 "viaCityNumbers": 0,
 "distance": 0.01,
 "trafficLights": 0,
 "tmcSegments": "",
 "totalOddDistance": "",
 "oddNum": 0,
 "time": 0.01,
 "tmcSize": 0,
 "tolls": 0,
 "method": "",
 "routePreference": 0,
 "newStrategy": -100,
 "distanceAuto": "",
 "timeAuto": ""
 }
 ],
 "fromPoiLongitude": 0.01,
 "resultCode": 10000,
 "toPoiAddr": "",
 "fromPoiAddr": "",
 "fromPoiLatitude": 0.01,
 "errorMessage": ""
 },
 "statusCode": 0,
 "needResponse": False,
 "message": "",
 "responseCode": "",
 "requestCode": "",
 "requestAuthor": "com.autonavi.amapauto"
}
    #dict2 = {"operaValue": 1, "resultCode": 10046, "actionType": 0, "operaType": 0, "errorMessage": ""}
    dict2 = {"data":[{"data":{"isCanZoom":True,"isSuccess":True,"operateType":4},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"curRoadName":""},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80057,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"locationInfo":"{\"accuracy\":10.0,\"bearing\":56.0,\"provider\":0,\"speed\":0.0,\"time\":{\"day\":12,\"hour\":2,\"minute\":31,\"month\":1,\"second\":34,\"year\":2022}}"},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80063,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"count":-1,"errorMessage":"\u8bf7\u6c42\u6210\u529f","resultCode":10000},"message":"","messageType":"response","needResponse":False,"protocolId":30400,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":4},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":4},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"curRoadName":""},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80057,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":3},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":2},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":3},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":4},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":3},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"curRoadName":""},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80057,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"locationInfo":"{\"accuracy\":10.0,\"bearing\":56.0,\"provider\":0,\"speed\":0.0,\"time\":{\"day\":12,\"hour\":2,\"minute\":32,\"month\":1,\"second\":55,\"year\":2022}}"},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80063,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"count":-1,"errorMessage":"\u8bf7\u6c42\u6210\u529f","resultCode":10000},"message":"","messageType":"response","needResponse":False,"protocolId":30400,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":4},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":4},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"curRoadName":""},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80057,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":3},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":2},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":1},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":4},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":3},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":4},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":3},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"curRoadName":""},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80057,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"locationInfo":"{\"accuracy\":10.0,\"bearing\":56.0,\"provider\":0,\"speed\":0.0,\"time\":{\"day\":12,\"hour\":2,\"minute\":34,\"month\":1,\"second\":15,\"year\":2022}}"},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80063,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"count":-1,"errorMessage":"\u8bf7\u6c42\u6210\u529f","resultCode":10000},"message":"","messageType":"response","needResponse":False,"protocolId":30400,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":4},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"},{"data":{"isCanZoom":True,"isSuccess":True,"operateType":4},"message":"","messageType":"dispatch","needResponse":False,"protocolId":80095,"requestAuthor":"com.aiways.autonavi","requestCode":"","responseCode":"","statusCode":200,"versionName":"5.0.7.601114"}]}

    # dict2 = {"id": "100", "name": "华为", "info": {"uid": "2020", "phoneName": ["一代", "Mate40"]}}
    noise_data = {}
    result = compare_data("", dict1, dict2, noise_data, 2)
    print(result)
    #print(get_return_msg(result))
    # {
    # "operaValue": 1,
    # "resultCode": 10000,
    # "actionType": 0,
    # "operaType": 0,
    # "errorMessage": ""
    # }
