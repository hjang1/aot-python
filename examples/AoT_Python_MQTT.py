# -*- coding: utf-8 -*-
'''
Copyright (c) 2017  ntels Co., LTD.

@author: Donghee Kim
'''

from time import sleep
import sys

from mqtt.client import AOTMqttClient


DeviceID = "D59850137584"            # 디바이스 인증정보(디바이스 ID)
DeviceKey = "e8d54baed5354575"       # 디바이스 인증정보(인증 헤더)
client = None

def deviceCmdOperation(data):

    if data[0] == "forward":
        print "[Result] deviceCmdOperation: Forwarded"
        return True
    else:
        print "[Result] deviceCmdOperation: Not defined"
        return False

def nodeCmdOperation(data):
    if data[0] == "stop":
        print "command message is accepted for [ node: " + data[1] + " ]"
        # NOTE: You can return any value that want responds to.
        return True
    elif data[0] == "start":
        print "command message is accepted for [ node: " + data[1] + " ]"
        # NOTE: You can return any value that want responds to.
        return True

    else:
        print "[Result] nodeCmdOperation: Not defined"
        return False


# Main function
if __name__ == "__main__":

    try:
        client = AOTMqttClient()
        client.setDeviceInfo(DeviceID, DeviceKey, deviceCmdOperation, nodeCmdOperation, tls=True)
        client.connect()

        while True:

            # Note: publish the device content
            client.publishDeviceContent(50)

            # Note: publish the node content
            client.publishNodeContent(1, 33.8)

            # Note: sleep for 1 second
            sleep(3)

    except KeyboardInterrupt:
        print("[log] main: Exiting Application")
        client.disconnect()
        sys.exit()
