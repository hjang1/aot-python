# -*- coding: utf-8 -*-
'''
Copyright (c) 2017  ntels Co., LTD.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Created on 2017. Feb. 20.

@author: asurada
'''
import json
from datetime import datetime
from collections import OrderedDict

class JSONEncoder(json.JSONEncoder):
    # @override
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat() + 'Z'
        elif hasattr(obj, '__getstate__'):
            return obj.__getstate__()
        else:
            return json.JSONEncoder.default(self, obj)

class MQTTModel:
    def __init__(self, deviceID=None, deviceKey=None):
        self.deviceID = deviceID
        self.deviceKey = deviceKey

    def getDeviceContentModelJson(self, contentValue=None):
        dic = OrderedDict()
        dic["message_type"] = "device.content"
        dic["device_id"] = self.deviceID
        dic["device_key"] = self.deviceKey
        dic["content_value"] = contentValue
        return json.dumps(dic, sort_keys=False, ensure_ascii=False)

    def getNodeContentModelJson(self, contentValue=None, nodeID=None):
        dic = OrderedDict()
        dic["message_type"] = "node.content"
        dic["device_id"] = self.deviceID
        dic["device_key"] = self.deviceKey
        dic["node_id"] = nodeID
        dic["content_value"] = contentValue
        return json.dumps(dic, sort_keys=False, ensure_ascii=False)

    def getdeviceResCmdModelJson(self, responseValue=None, commandID=None):
        dic = OrderedDict()
        dic["message_type"] = "device.cmd"
        dic["device_id"] = self.deviceID
        dic["device_key"] = self.deviceKey
        dic["command_id"] = commandID
        dic["response_value"] = responseValue
        return json.dumps(dic, sort_keys=False, ensure_ascii=False)

    def getNodeResCmdModelJson(self, responseValue=None, nodeID=None, commandID=None):
        dic = OrderedDict()
        dic["message_type"] = "node.cmd"
        dic["device_id"] = self.deviceID
        dic["device_key"] = self.deviceKey
        dic["node_id"] = nodeID
        dic["command_id"] = commandID
        dic["response_value"] = responseValue
        return json.dumps(dic, sort_keys=False, ensure_ascii=False)



