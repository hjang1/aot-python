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

import sys, os
from time import sleep
import Adafruit_DHT                                                                     #온습도 센서 (DHT11)를 사용하기 위한 라이브러리 ( 설치 필요 )

os.chdir(os.path.dirname( os.path.abspath( __file__ ) ))
sys.path.insert(0, '../')                                                               # 상위 디렉토리의 파일을 사용하기 위해 경로 변경     

from rest.client import AOTHtmlClient

DeviceID        = "D41050139110"                #디바이스 인증정보(디바이스 ID)
DeviceKey       = "Basic RDQxMDUwMTM5MTEwOjI0YzFhNjM0YzczYTRkYWU="    #디바이스 인증정보(인증 헤더)
ID_Temperature  = "1"                           #서버에 등록된 센서 ID (온도)
ID_Humidity     = "2"                           #서버에 등록된 센서 ID (온도)
PIN_DHT         = 25                            #온.습도센서(DHT11)의 GPIO 핀 번호

# 메세지 전송
def sendMessage(nodeID, data):
    print str(data),
    if client.sendMessage(nodeID, data):          
        print " sendMessage success"
    else:
        print" sendMessage fail"

# 메인
if __name__ == "__main__":      
    client = AOTHtmlClient()
    client.setDeviceInfo(DeviceID, DeviceKey)   # 단말기 정보를 등록한다.  (서버->디바이스->디바이스 인증정보->디바이스 아이디, 인증 헤더)  

    try:
        while True:                                                                     # 무한 반복 
            try:
                humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, PIN_DHT)   # 온도, 습도를 가지고 온다.
                if humidity is not None and temperature is not None:
                    print "Temperature ",     
                    sendMessage(ID_Temperature, temperature)                            #온도 값 전송
                    print "Humidity ",    
                    sendMessage(ID_Humidity, humidity)                                  #습도 값 전송
                else:
                    print 'Failed to get reading. Try again!'
            except Exception as exc:
                break
            sleep(1)                                                                    #업데이트 주기 1초   
            
    except KeyboardInterrupt:
        # quit
        print 'Exiting application'
        sys.exit()
        
    except Exception as exc:
        print exc
        
