# -*- coding: utf-8 -*-
'''
Copyright (c) 2017  ntels Co., LTD.

@author: Donghee Kim
'''

from time import sleep
import sys

from mqtt.client import AOTMqttClient

DeviceID = "xxx"  # 디바이스 인증정보(디바이스 ID)
DeviceKey = "xxx"  # 디바이스 인증정보(인증 헤더)
client = None

"""
@Function: deviceCmdOperation
@Param: data - requested command data.
@Return: You can return any value that want responds to.
@Explain: This function is called, if device command request message arrived.
"""
def deviceCmdOperation(data):
    if data[0] == "forward":
        print "[Result] deviceCmdOperation: Forwarded"
        return True
    else:
        print "[Result] deviceCmdOperation: Not defined"
        return False

"""
@Function: deviceCmdOperation
@Param: data - requested command data.
@Return: You can return any value that want responds to.
@Explain: This function is called, if node command request message arrived.
"""
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
        # NOTE: get AOT MQTT Client
        client = AOTMqttClient()
        # NOTE: set Device information to connect the AoT server.
        client.setDeviceInfo(DeviceID, DeviceKey, deviceCmdOperation, nodeCmdOperation, tls=True)
        # NOTE: Starts to connect
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
