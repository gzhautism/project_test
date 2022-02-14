import json
import time

import requests

url = 'http://10.130.160.110:5000/pc/senddata'
# url = 'http://127.0.0.1:5000/pc/senddata'

n = 1000
k = 0
# params = {
#     "protocolId": 30000,
#     "messageType": "request",
#     "versionName": "v_20200320",
#     "data": {
#     "operaValue": 1,
#     "tempValue": "",
#     "operaType": 0,
#     "actionType": 0
#     },
#     "statusCode": 0,
#     "needResponse": True,
#     "message": "",
#     "responseCode": "",
#     "requestCode": "",
#     "requestAuthor": "com.aiways.aiwaysservice"
#     }
"""
params = {
  "protocolId": 30402,
  "messageType": "request",
  "versionName": "v_20200320",
  "data": {
    "endProtocolPoi": {
      "poiName": "武汉站",
      "midtype": 0,
      "longitude": 114.424314,
      "address": "",
      "poiId": "",
      "nTypeCode": "",
      "entryLatitude": 0.01,
      "entryLongitude": 0.01,
      "latitude": 30.606697
    },
    "startProtocolPoi": {
      "poiName": "",
      "midtype": 0,
      "longitude": 114.410493,
      "address": "",
      "poiId": "",
      "nTypeCode": "",
      "entryLatitude": 0.01,
      "entryLongitude": 0.01,
      "latitude": 30.482407
    },
    "newStrategy": 9,
    "strategy": -1,
    "actionType": 4,
    "dev": 0,
    "midProtocolPois": [
      {
        "poiName": "光谷第四小学",
        "midtype": 0,
        "longitude": 114.427331,
        "address": "",
        "poiId": "",
        "nTypeCode": "",
        "entryLatitude": 0.01,
        "entryLongitude": 0.01,
        "latitude": 30.508395
      }
    ]
  },
  "statusCode": 0,
  "needResponse": True,
  "message": "",
  "responseCode": "",
  "requestCode": "",
  "requestAuthor": "com.aiways.aiwaysservice"
}
"""



params = {
 "protocolId": 30305,
 "messageType": "request",
 "versionName": "5.0.7.601114",
 "data": {
 "maxCount": 30
 },
 "statusCode": 0,
 "needResponse": True,
 "message": "",
 "responseCode": "",
 "requestCode": "",
 "requestAuthor": "com.aiways.aiwaysservice"
}

a = requests.post(url=url, data=json.dumps({"data": params}))
print(a.text)

