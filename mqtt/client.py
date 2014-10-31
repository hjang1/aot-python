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
'''
import datetime
from collections import OrderedDict
from util.models import mqttMessageModel
from util.models import mqttResponseModel
from paho.mqtt.client import Client as mqttClient
import json

class AOTMqttClient:
    
    def __init__(self):
        self.client = mqttClient()
        self.connected = False                              # 접속 여부
        self.deviceID = None                                # 디바이스 아이디
        self.deviceKey = None                               # 디바이스 토큰    
        self.publish_topic = None                           # 메세지 발신 토픽
        self.subscribe_topic = None                         # 메세지 수신 토픽
        self.client.on_connect = self.__on_connect          # 브로커 서버에 접속 성공했을 때 호출되는 콜백
        self.client.on_disconnect = self.__on_disconnect    # 브로커 서버에 접속이 끊겼을 때 호출되는 콜백
        self.client.on_message = self.__on_message          # 브로커 서버로 부터 메세지를 수신 받았을 때 호출 되는 콜백     
        self.callBack = None;
    
    # 관리페이지에서 할당받은 디바이스 인증정보(디바이스 = > 디바이스 인증정보).         
    def setDeviceInfo(self, deviceID, deviceKey, callBack):
        try:
            self.deviceID = deviceID
            self.deviceKey = deviceKey
            self.callBack = callBack
            self.client.username_pw_set(deviceID, deviceKey)
            self.publish_topic = "/" + str(deviceID) + "/publish"
            self.subscribe_topic = "/" + str(deviceID) + "/subscribe"
        except Exception as exc:
            print exc
            
    def connect(self):
        if self.connected :
            return True
        
        try:
            if self.client.connect("api.allofthings.com", 1883, 1) == 0 :
                self.client.loop_start()
                return True
        except Exception as exc:
            print exc,
            return False
                        
    def disconnect(self):
        self.client.loop_stop(True)        
        if self.connected:
            self.client.disconnect()
        self.connected = False  
    
    #브로커 서버에 메세지를 전달 한다.
    def sendMessage(self, nodeId, msg):
        if self.connected :
            model = mqttMessageModel(self.deviceID, self.deviceKey, nodeId, msg)
            self.client.publish(self.publish_topic, model.getMqttMessageModelJson())
        else:
            self.connect()     
            
        return self.connected

    # 접속 시도후 결과값 반환 ( 성공, 실패 상관없이 호출됨 )
    def __on_connect(self, client, userdata, sp, rc):        
        if rc == 0: #접속 성공시
            self.connected = True
            self.client.subscribe(self.subscribe_topic)
        else:
            self.connected = False

    def __on_disconnect(self,client, userdata, rc):
        self.connected = False  

    
    #서버로부터 메세지 수신
    def __on_message(self, client, userdata, message):
        msg = message.payload
        if self.callBack != None:
            try:
                loadJsonMsg = json.loads(msg.decode("UTF-8"))
                nodeId = loadJsonMsg["node_id"]
                commandId = loadJsonMsg["command_id"]
                
                result = self.callBack(nodeId, commandId, loadJsonMsg["request_value"])
                
                command_status = "D_SUCCESS"
                if result[0] == False:
                     command_status = "D_FAIL"
                
                model = mqttResponseModel(self.deviceID, self.deviceKey, str(nodeId), str(commandId), command_status, result[1])
                self.client.publish(self.publish_topic, model.getMqttResponseModelJson())
                
            except Exception as exc:
                print exc
        else:
            print "serverDataCallBack Method is not defined."
        