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
'''
from util.models import MQTTModel
import paho.mqtt.client as mqtt
import json
from time import sleep


class AOTMqttClient:
    def __init__(self):
        self.HOST = "api.allofthings.com"                   # Host IP
        self.PORT = 1883                                    # Port address
        self.QOS = 1                                        # MQTT Qos level
        self.KEEPALIVE = 60                                 # Keep alive time

        self.client = mqtt.Client()
        self.connected = False                              # To check success or failure
        self.deviceID = None                                # Device ID
        self.deviceKey = None                               # Device Token
        self.publish_topic = None                           # Publish Topic
        self.subscribe_topic = None                         # Subscribe Topic
        self.client.on_connect = self.__on_connect          # Callback when connected to Broker
        self.client.on_disconnect = self.__on_disconnect    # Callback when disconnected from Broker
        self.client.on_message = self.__on_message          # Callback when message received from Broker
        self.client.on_publish = self.__on_publish          # Callback after successfully published
        self.deviceCallBack = None
        self.nodeCallBack = None
        self.mqttModel = None                               # MQTT message container


    # TLS is not supportable on this version
    def setDeviceInfo(self, deviceID, deviceKey, d_callBack, n_callback, tls=False):
        try:
            self.mqttModel = MQTTModel(deviceID, deviceKey)
            self.deviceCallBack = d_callBack
            self.nodeCallBack = n_callback
            self.client.username_pw_set(deviceID, deviceKey)
            self.publish_topic = "/" + str(deviceID) + "/publish"
            self.subscribe_topic = "/" + str(deviceID) + "/subscribe"

            # if tls:
            #     self.client.tls_set()


        except Exception as e:
            print "[error setDeviceInfo] Exception: " + e.__str__()

    """
    @Method: connect()
        This method tries to connect the MQTT broker as sync mode or async mode.
        Default mode is sync mode.
    @Param
        mode - Defines sync mode or async mode.
    @Return
        None
    @Note
        Async mode is not supported on this version.
    """

    def connect(self, mode="Sync"):
        if self.connected is not True:
            if mode == "Sync":

                self.client.connect(self.HOST, self.PORT, self.KEEPALIVE)
                self.on_listen()
                sleep(1)
                print "[Log] connect: Sync connection Success"


            elif mode == "Async":
                self.client.connect_async(self.HOST, self.PORT, self.KEEPALIVE)
                print "[Log] connect: Async connection Success"
        else:
            print "[Log] connect: connection fail"

    """
    @Method: on_listen()
        Start listening from network.
    @Param
        timeout - This function blocks for up to timeout seconds.
                - Timeout must not exceed the keepalive value for the client.
    @Return
        None
    @NOTE
        timeout mode is not supported on this version.
    """

    def on_listen(self, timeout=0):
        if timeout == 0:
            self.client.loop_start()
        else:
            self.client.loop(timeout)

    """
    @Method: off_listen()
        Stop listening from network.
    @Param
        None
    @Return
        None
    """

    def off_listen(self):
        self.client.loop_stop(True)

    """
    @Method: disconnect()
        Disconnect the connection and stop listening packet from network.
    @Param
        None
    @Return
        None
    """

    def disconnect(self):
        self.off_listen()
        self.client.disconnect()

    """
    @Method: publishDeviceContent
        This method publish the content using device.content model.
    @Param
        content: device content information
    @Return
        None
    """

    def publishDeviceContent(self, content):
        if self.connected:
            self.client.publish(self.publish_topic,
                                self.mqttModel.getDeviceContentModelJson(content))
        else:
            print "[log] publishDeviceContent : Waiting for connection."


    """
    @Method: publishNodeContent
        This method publish the node or sensor content using node.content model.
    @Param
        nodeID: node ID
        content: node content information
    @Return
        None
    """

    def publishNodeContent(self, nodeID, content):
        if self.connected:
            self.client.publish(self.publish_topic,
                                self.mqttModel.getNodeContentModelJson(content, nodeID))
        else:
            print "[log] publishNodeContent : Waiting for connection."


            ####### Callback definition from here. #######

    """
    @Callback Method: __on_connect()
        This method is called after connect().
    @Param
        client - the client instance for this callback
        userdata - the private user data as set in Client() or userdata_set()
        flags - response flags sent by the broker
        rc - the connection result
    @Return
        None
    """
    def __on_connect(self, client, userdata, flags, rc):
        self.connected = False
        if rc == 0:  # 접속 성공시
            self.connected = True
            # self.on_listen()           # network thread on
            self.client.subscribe(self.subscribe_topic)
        else:  # 접속 실패시 에러 메세지
            self.errorMessages(("on_connect", rc))

    """
    @Callback Method: __on_disconnect()
        This method is called after disconnect().
    @Param
        client - the client instance for this callback
        userdata - the private user data as set in Client() or userdata_set()
        rc - the connection result
    @Return
        None
    """

    def __on_disconnect(self, client, userdata, rc):
        self.HOST = None  # Host IP
        self.PORT = None  # Port address
        self.QOS = None  # MQTT Qos level
        self.KEEPALIVE = None  # Keep alive time
        self.client = None
        self.connected = False  # 접속 여부
        self.deviceID = None  # 디바이스 아이디
        self.deviceKey = None  # 디바이스 토큰
        self.publish_topic = None  # 메세지 발신 토픽
        self.subscribe_topic = None  # 메세지 수신 토픽
        self.callBack = None
        print "[log] __on_disconnect: Successfully Disconnected."

    """
        @Callback Method: __on_publish()
            This method is called after publish method.
            This callback is important because even if the publish() call returns success,
            it does not always mean that the message has been sent.
        @Param
            client - the client instance for this callback
            userdata - the private user data as set in Client() or userdata_set()
            mid - transaction ID when data is published.
        @Return
            None
    """

    def __on_publish(self, client, userdata, mid):
        # You may override on_publish callback method
        print "[log] publishDeviceContent : Success to publish " + self.publish_topic

    """
        @Callback Method: __on_message()
            This method is called when message arrived from the broker.
            This method linked into customer callback function.
            The response will immediately publish after transaction.
        @Param
            client - the client instance for this callback
            userdata - the private user data as set in Client() or userdata_set()
            message - received message in JASON format.
        @Return
            None
    """

    def __on_message(self, client, userdata, message):
        msg = message.payload

        try:
            loadJsonMsg = json.loads(msg.decode("UTF-8"))

            if loadJsonMsg["message_type"] == "device.cmd":

                # NOTE: Set the value.
                deviceKey = loadJsonMsg["device_key"]
                commandId = loadJsonMsg["command_id"]
                requestValue = loadJsonMsg["request_value"]

                # NOTE: Get command amd forward to callback.
                deviceCmd = (requestValue, deviceKey, commandId)
                result = self.deviceCallBack(deviceCmd)

                # NOTE: Publish the response
                self.client.publish(self.publish_topic, self.mqttModel.getdeviceResCmdModelJson(result, commandId))

            elif loadJsonMsg["message_type"] == "node.cmd":
                # NOTE: Set the value.
                deviceKey = loadJsonMsg["device_key"]
                commandId = loadJsonMsg["command_id"]
                requestValue = loadJsonMsg["request_value"]
                nodeID = loadJsonMsg["node_id"]

                # NOTE: Get command amd forward to callback.
                nodeCmd = (requestValue, nodeID, deviceKey, commandId)
                result = self.nodeCallBack(nodeCmd)

                # NOTE: Publish the response
                self.client.publish(self.publish_topic, self.mqttModel.getNodeResCmdModelJson(result, nodeID, commandId))

            else:
                print "[Warning] __on_message: Unknown Message type!"

        except Exception as exc:
            print exc
