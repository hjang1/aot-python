# aot-python

AoT와 연동하기 위한 오픈 하드웨어 개발용 Python 라이브러리 및 예제 소스입니다. 
MQTT 통신을 이용하여 센서값을 publish하고 명령어(command)를 subscribe 합니다.
   
## Getting Started

본 스크립트는 python 2 version을 기준으로 작성되었습니다. 따라서 사전에 [python2](https://www.python.org/downloads/)가 설치되어있어야합니다.

### Installing

파일을 다운 받은 후 다음 명령어를 실행하여 모듈을 설치합니다.

```
python setup.py install
```

### Running the tests

Example directory에 있는 샘플 코드를 다음 명령어를 입력하여 실행합니다.

```
python AoT_Python_MQTT.py
```

정상적으로 실행 될 경우 
```
[Log] connect: Sync connection Success
[log] publishDeviceContent : Success to publish /D59850137584/publish
[log] publishDeviceContent : Success to publish /D59850137584/publish
```
위와 같은 로그를 출력합니다.

## Authors

* **Donghee Kim** - *nTels Researcher* - [All of Things](https://github.com/ntels-aot)
* **Huk Jang** - *nTels Researcher* - [All of Things](https://github.com/ntels-aot)
