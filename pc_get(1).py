import json
import time

import requests

# url = 'http://127.0.0.1:5000/app/getdata'
url = 'http://10.130.160.110:5000/pc/getdata'
a = requests.get(url=url)
print(a.text)
# def get_return_json(id, data, is_input):
#     data = json.loads(data.text).get('data', [])
#     json_data = {}
#     data.reverse()
#     for i in data:
#         if is_input and str(id) == str(i.get("protocolId", "")) and i.get("messageType", '') == "response":
#             json_data = i
#             break
#         elif str(id) == str(i.get("protocolId", "")) and i.get("messageType", '') == "dispatch":
#             json_data = i
#             break
#     return json_data
#
#
# print(get_return_json(30402, a, True))

"""
"{\n  \"protocolId\": 40005,\n  \"messageType\": \"request\",\n  \"versionName\": \"v_20200320\",\n  \"data\": {\n    \"type\": 4,\n    \"sort\":  4\n  },\n  \"statusCode\": 0,\n  \"needResponse\": false,\n  \"message\": \"\",\n  \"responseCode\": \"\",\n  \"requestCode\": \"\",\n  \"requestAuthor\": \"com.aiways.aiwaysservice\"\n}"
"{\n  \"protocolId\": 40005,\n  \"messageType\": \"request\",\n  \"versionName\": \"5.0.7.601114\",\n  \"data\": {\n    \"type\": 4,\n    \"sort\":  4\n  },\n  \"statusCode\": 0,\n  \"needResponse\": false,\n  \"message\": \"\",\n  \"responseCode\": \"\",\n  \"requestCode\": \"\",\n  \"requestAuthor\": \"com.aiways.autonavi\"\n}"
"""