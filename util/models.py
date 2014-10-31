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

@author: asurada
'''
import json
from datetime import datetime
from collections import OrderedDict


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat() + 'Z'
        elif hasattr(obj, '__getstate__'):
            return obj.__getstate__()
        else:
            return json.JSONEncoder.default(self, obj)
        

# mqtt 전송 (센서 값 전송)  
class mqttMessageModel():
    def __init__(self, deviceId = None, deviceKey = None, nodeId = None, contentValue = None):
        self.message_type = "node.content"    
        self.deviceId = deviceId
        self.deviceKey = deviceKey               
        self.nodeId = nodeId
        self.contentValue  = contentValue

    
    
    def getMqttMessageModel(self):
        dic = OrderedDict()
        
        dic["message_type"] = self.message_type
        
        if self.deviceId != None:
            dic["device_id"] = self.deviceId
        
        if self.deviceKey != None:
            dic["device_key"] = self.deviceKey
        
        if self.nodeId != None:
            dic["node_id"] = self.nodeId
        
        if self.contentValue != None:
            dic["content_value"] = self.contentValue
            
        return dic
    
    
    def getMqttMessageModelJson(self):
        model = self.getMqttMessageModel()
        return json.dumps(model, sort_keys = False, ensure_ascii=False)
  
# mqtt 전송 ( 제어 결과 전송 )
class mqttResponseModel():
    def __init__(self, deviceId = None, deviceKey = None, nodeId = None, commandId = None, commandStatus = None, additionMessage = None):
        self.message_type       = "node.cmd"    
        self.deviceId           = deviceId
        self.deviceKey          = deviceKey               
        self.nodeId             = nodeId
        self.commandId          = commandId
        self.commandStatus      = commandStatus
        self.additionMessage    = additionMessage

    def getMqttResponseModel(self):
        dic = OrderedDict()
        
        dic["message_type"] = self.message_type
        
        if self.deviceId != None:
            dic["device_id"] = self.deviceId
        
        if self.deviceKey != None:
            dic["device_key"] = self.deviceKey
        
        if self.nodeId != None:
            dic["node_id"] = self.nodeId
        
        if self.commandId != None:
            dic["command_id"] = self.commandId
        
        if self.commandStatus != None:
            dic["command_status"] = self.commandStatus
            
        if self.additionMessage != None:
            dic["addition_message"] = self.additionMessage
            
        return dic
    
    
    def getMqttResponseModelJson(self):
        model = self.getMqttResponseModel()
        return json.dumps(model, sort_keys = False, ensure_ascii=False)
    

# rest 전송 (센서 값 전송)    
class restMessageModel():
    def __init__(self, contentValue = None):
        self.contentValue  = contentValue

    def getRestMessageModel(self):
        dic = OrderedDict()
        
        if self.contentValue != None:
            dic["content_value"] = self.contentValue
            
        return [dic]
    
    
    def getRestMessageModelJson(self):
        model = self.getRestMessageModel()
        
        return json.dumps(model, sort_keys = False, ensure_ascii=False)
    