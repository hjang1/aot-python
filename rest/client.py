# -*- coding: utf-8 -*-
'''
Copyright (c) 2014  ntels Co., LTD.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and 
limitations under the License.

Created on 2014. 9. 2.
'''

import requests 
import datetime
from collections import OrderedDict
from util.models import restMessageModel

host = "https://api.allofthings.com"
port = 5003

class AOTHtmlClient: 
    def __init__(self):
        self.request = None
        self.url = None                             # 서버 url
        self.deviceID = None                        # 디바이스 아이디
        self.deviceKey = None                       # 디바이스 토큰    
        self.httpHeader = {}
        self.httpHeader["Content-Type"] = "application/json"

    def setDeviceInfo(self, deviceId, auth):
        self.url = host + ":" + str(port) + "/devices/" + deviceId + "/nodes"
        self.deviceID = deviceId
        self.auth = auth
        self.httpHeader["Authorization"] = self.auth
    
    # 메세지 전송
    def sendMessage(self, sensorName, sensorValue):
        try:
            json = restMessageModel(sensorValue).getRestMessageModelJson()            # json 생성
            response = requests.post(self.url + "/" + sensorName + "/contents", data=json, headers=self.httpHeader)
            code = response.status_code
            if code == 201:
                return True
        except Exception as exc:
            print exc,
        return False
