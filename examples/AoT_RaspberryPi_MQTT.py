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

from time import sleep
import sys, os
import Adafruit_DHT         #온습도 센서 (DHT11)를 사용하기 위한 라이브러리 ( 설치 필요 )
import RPi.GPIO as GPIO

os.chdir(os.path.dirname( os.path.abspath( __file__ ) ))
sys.path.insert(0, '../')                                                               # 상위 디렉토리의 파일을 사용하기 위해 경로 변경 
from mqtt.client import AOTMqttClient 

DeviceID        = "D67379307011"                #디바이스 인증정보(디바이스 ID)
DeviceKey       = "ff6915411a5c4fce"            #디바이스 인증정보(인증 헤더)
ID_Temperature  = "3"                           #서버에 등록된 센서 ID (온도)
ID_Humidity     = "4"                           #서버에 등록된 센서 ID (습도)
ID_Control      = "5"                           #서버에 등록된 센서 ID (제어)
PIN_DHT         = 25                            #온.습도센서(DHT11)의 GPIO 핀 번호
PIN_LED         = 4                            #LED의 GPIO 핀 번호

#MQTT 브릿지 서버로부터 메세지를 전달받았을 경우 콜백되는 함수로 명령을받아 제어한후 제어 결과와 사용자 메세지를 리턴한다.
def callback(nodeID, commandID, command):
    if ID_Control == nodeID:
        if command == "true":
            GPIO.output(PIN_LED, True)          # LED 제어 (ON)
            return True, "led on"
        elif command == "false":
            GPIO.output(PIN_LED, False)         # LED 제어 (OFF)
            return True, "led off"
    else:
        return False, "led control fail"

# 메세지 전송
def sendMessage(nodeID, data):
    print str(data),
    if client.sendMessage(nodeID, data):          
        print " sendMessage success"
    else:
        print" sendMessage fail"

# 메인
if __name__ == "__main__":
    client = AOTMqttClient()
    client.setDeviceInfo(DeviceID, DeviceKey, callback)     # 단말기 정보(서버->디바이스->디바이스 인증정보->디바이스ID, 디바이스 토큰) 및 서버 콜백 함수를 등록 한다.

    GPIO.setmode(GPIO.BCM)                                  # GPIO 핀 번호를 사용하기위한 모드 설정
    GPIO.setup(PIN_LED, GPIO.OUT)                           # 제어용 센서 설정

    try:
        while True:                                                                     # 무한 반복 
            try:
                humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, PIN_DHT)   # 온도, 습도를 가지고 온다.
                if humidity is not None and temperature is not None:                    # 온도와 습도를 정상적으로 가지고 왔을 경우 
                    print "Temperature ",   
                    sendMessage(ID_Temperature, temperature)                            # 온도 값 전송
                    print "Humidity ",
                    sendMessage(ID_Humidity, humidity)                                  # 습도 값 전송
                else:       
                    print 'Failed to get reading. Try again!'
                sleep(1)                                                                # 업데이트 주기 1초   
            except Exception as exc:                                                    
                break
    except KeyboardInterrupt:                                                           # 강제 종료시 콜백 (Ctrl + C)
        print('Exiting application')
        GPIO.cleanup()                                                                  # 센서 초기화
        sys.exit()
    except Exception as exc:
        print(exc)