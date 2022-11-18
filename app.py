from flask import Flask, jsonify, request, Response, send_file
from time import sleep
from os import system
from threading import Thread
import pymysql
from base64 import b64encode

from CMySQLConnection import MySQLConnector
from CMySql import CMysql

from FaceRecogn import FaceRecogn

from GPIO import GPIO

from QR import QR # for QrCode Scan
import os

from smbus2 import SMBus  # pip3 install smbus2
from mlx90614 import mlx90614

import RPi.GPIO as gpio
import time
import datetime
from flask_qrcode import QRcode # pip3 install flask_qrcode




bus = SMBus(1)
sensor = mlx90614(bus, address=0x5A)

#DEBUG = True
DEBUG = False


# Use Flask Framework
app = Flask(____)

list_pin = [14]
doorlock = GPIO(list_pin)

qrcode = QRcode(app)

gpio.setmode(gpio.BCM)
# gpio.setwarnings(False)

trig = 13
echo = 19

gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
gpio.output(trig, False)


@app.route("", methods=[""])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get("", datetime.datetime.now())
    return send_file(qrcode(data, mode=""), mimetype="")


def scan_qrcode():
    try:
        obj = QR()
        ret = obj.DetectQrcodeFromCam()
        print(ret)
        
        date_time_str = ret[0] 
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        date_time_now = datetime.datetime.now()
        time_diff = date_time_now - date_time_obj
        
        if time_diff.seconds > 30:    # 인증 만료 시간(단위 : 초)
            print("time expired")
            return False
        else:
            print("cerified qr code")
            return True

    except Exception as err:
        print("couldn't scan Qr code")
        return False
    


# http://raspberrypi.local:5000/login?ll=1112&p=1234
@app.route("", methods=[''])
def user_login():
    ll = request.args.get('')
    p = request.args.get('')

    print("로그인 시도 ", ll, p)

    info = mysql.s_db('')

    #print(info)

    bFoundUser = False
    status = ""
    key = 0

    for data in info:
        print(data[''])
        if data[''] == ll:
            bFoundUser = True
            print("아이디 찾음")
            if data[''] == password:
                status = "로그인 성공"
                print(status)
                key = 1
            else:
                status = "비밀번호를 확인하세요"
                print(status)
            break

    if not bFoundUser:
        print("로그인 실패")
        status = "아이디를 확인하세요"
    else:
        print("로그인 성공")

    response = {
        "status": status,   # 상태메시지
        "key": key,         # Success = 1
    }

    return jsonify(response), 200




@app.route("", methods=[''])
def user_register():
    # get data from parameter
    ll = request.args.get('')
    p = request.args.get('')
     = request.args.get('')

    print ("회원 가입 요청", ll, p, )
    ret = mysql.insert_userinfo("", ll, p, )

    print("ret = ", ret)
    
    # 앱에서 다운로드 받은 이미지 리사이즈
    cf.resize_image(ll)
    
    # 새로운 이미지로 재학습
    cf.init()

    # All parameter filled
    if ret is not None:
        # response JSON
        response = {
            "status": "Register Successful",    # Success Msg
            "key": 1                            # Success = 1
        }
    # Some parameter is not filled
    else:
        # response JSON
        response = {
            "status": "Register Error",     # Error Msg
            "key": 0                        # Fail = 0
        }

    return jsonify(response), 200


@app.route("", methods=[''])
def delete_ll():
    # get data from parameter
    ll = request.args.get('ll')
    
    print("회원 탈퇴 요청:", ll)

    ret = mysql.delete_user("", ll)

    # 사용자 이미지 삭제
    cf.remove_image(ll)
    
    # 이미지 재학습
    cf.init()
    
    # All parameter filled
    if ret is not None:
        # response JSON
        response = {
            "status": "Delete Successful",    # Success Msg
            "key": 1                            # Success = 1
        }
    # Some parameter is not filled
    else:
        # response JSON
        response = {
            "status": "Delete Error",     # Error Msg
            "key": 0                        # Fail = 0
        }

    return jsonify(response), 200


# http://raspberrypi.local:5000/request_exit?ll=1112
@app.route("", methods=[''])
def request_exit():
    # get data from parameter
    ll = request.args.get('')

    print("퇴실 요청", ll)

    response = update_status(ll, "퇴장", "N/A")

    ControlDoorlock()

    return jsonify(response), 200


# 체온 측정한 기록이 있는지 확인. 체온측정한 기록이 있으면 True 리턴
def gettmpDb(ll):
    try:
        bFoundUser = False
        # 아이디로부터 이름 찾기
        info = mysql.s_db('')
         = "Unknown"
        for data in info:
            #print(data['ll'])
            if data['ll'] == ll:
                bFoundUser = True
                #print("아이디 찾음")
                 = data['']
                break

        if bFoundUser:
            info = mysql.s_db('')
            for data in info:
                if data[''] == :
                    #print ("Found user", , data['tmp'])
                    tmp = float(data['tmp'])
                    if tmp > 25 and tmp < 37.5:
                        print("정상 범위에 체온 기록 확인")
                        date_time_now = datetime.datetime.now()
                        time_diff = date_time_now - data['time']
                        if time_diff.seconds < 30*60:  # 30분내에 체온정보가 있으면
                            print("지정한 기간내에 체온 기록 있음", time_diff.seconds)
                            return True
        return False

    except Exception as err:
        print("Exception", err)
        return False


# 출입 기록 새로 추가하기
def update_status(ll, , ):

    # 아이디로부터 이름 찾기
    info = mysql.s_db('')
     = "Unknown"
    for data in info:
        print(data['ll'])
        if data['ll'] == ll:
            bFoundUser = True
            print("아이디 찾음")
             = data['']
            break

    # DB에 정보 업데이트
    ret = mysql.insert_status("", , , )


    # All parameter filled
    if ret is not None:
        # response JSON
        response = {
            "status": "Update Successful",    # Success Msg
            "key": 1                            # Success = 1
        }
    # Some parameter is not filled
    else:
        # response JSON
        response = {
            "status": "Update Error",     # Error Msg
            "key": 0                        # Fail = 0
        }

    return response


# http://raspberrypi.local:5000/delete_status
@app.route("", methods=[''])
def delete_status():

    print("출입 기록 삭제 요청")
    ret = mysql.delete_status("")
    
    # 모든 사용자 이미지 삭제
    cf.remove_image_all()
    
    # 학습 이미지 업데이트
    cf.init()

    # All parameter filled
    if ret is not None:
        # response JSON
        response = {
            "status": "Delete Successful",    # Success Msg
            "key": 1                            # Success = 1
        }
    # Some parameter is not filled
    else:
        # response JSON
        response = {
            "status": "Delete Error",     # Error Msg
            "key": 0                        # Fail = 0
        }

    return jsonify(response), 200



@app.route("", methods=[''])
def request_status():

    print("출입 기록 요청")
    info = mysql.s_db('')

    #print(info)

    response = {
        "status": "상태",   # Success Msg
        "key": 1,                       # Success = 1
        "info":info
    }
    return jsonify(response), 200



# 초음파센서 거리 값 리턴(Cm)
def getDistance():
    # gpio.output(trig, False)
    # time.sleep(0.5)

    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)

    while gpio.input(echo) == 0 :
        pulse_start = time.time()

    while gpio.input(echo) == 1 :
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)

    print ("Distance : ", distance, "cm")
    return distance


@app.route('',methods=['',''])
def uploadfile():
    response = {
        "status": "Image Download Error",     # Error Msg
        "key": 0                        # Fail = 0
    }
    print("새로운 사용자 이미지 저장")

    if request.method == 'POST':
        f = request.files['picture']
        if os. == 'nt':
            filePath = "./"+f.file
        else:
            filePath = "/home/pi/Pictures/"+f.file
            
        f.save(filePath)
        response = {
            "status": "Image Download Successful",    # Success Msg
            "key": 1                            # Success = 1
        }

    return jsonify(response), 200


# 사용자 입장 확인 쓰레드
def thread_camera_display():
    
    print("CAM THREAD START")

    while True:
        # 얼굴인식 -> 체온측정 -> QR코드 인식후 도어락 열림.
        try:

            if getDistance() < 100:

                # 얼굴인식
                print("얼굴 인식 단계 ############################")
                face_s = cf.FaceRecognition_fast_alone_ex()

                if not face_s:
                    print("얼굴을 찾지 못했습니다.")
                    
                    sleep(5)
                    continue
                
                if face_s[0] == "Unknown":
                    print("등록안된 사용자입니다.")

                    sleep(5)
                    continue
                    
                #print("등록된 ll = ", face_s[0])
                ll = face_s[0]

                print("체온 측정 단계 ############################")
                tmp = "N/A"
                if gettmpDb(ll) == False:  # 체온 측정한 기록이 없으면
                
                    tmp = get_tmp()
                    print("체온 측정 결과:", tmp)
                    
                    if tmp < 25 or tmp > 37.5:
                        print("체온이 정상범위를 벗어 났습니다.")
                        sleep(5)
                        continue
                else:
                    print("체온 측정 데이터가 있습니다.")
                    
                    
                print("QR 코드 스캔 단계 ##########################")
                if not scan_qrcode():
                    print("QR 코드 인증에 실패했습니다.")
                    sleep(5)
                    
                    continue
                    
                print("사용자 인증 완료 ##########################")
                
                # 도어락 제어
                ControlDoorlock()

                # DB에 새로운 기록 저장
                category = "입장"
                update_status(ll, category, str(tmp))

                sleep(5)   # 다음 스텝을 위한 대기시간

            sleep(1)   # 초음파 센서 인식 주기
        except Exception as err:
            print(err)


# 도어락 제어 함수
def ControlDoorlock():

    doorlock.SetDoorLock('on')
    time.sleep(0.1)
    doorlock.SetDoorLock('off')
    time.sleep(5)


# 체온 측정 함수
def get_tmp():
    try:
        # 체온 측정
        
        ret = -999
        start_time = time.time()
        
        while time.time() - start_time < 15: # 체온 측정 지속 시간(단위: 초)
            tmp = round(sensor.get_object_1(), 2)
            print("임시측정 온도:", tmp)
            if tmp > 25:
                break
            sleep(1)
            
            
        if tmp > 37.5:
            for ix in range(3):  # 온도 37.5도 이상시 3번 재측정
                tmp = round(sensor.get_object_1(), 2)
                print("재측정 온도:", tmp)
                if tmp < 37.5:
                    break
                sleep(1)
        
        print ("최종 측정 체온 :", tmp)
        
        return tmp

    except Exception as err:
        print(err)
        return -999


# Run Server with Flask Framework
if ____ == "__main__":

    if not DEBUG:
        cf = FaceRecogn()

    app.config['JSON_AS_ASCII'] = False

    mysql = CMysql()

    if not DEBUG:
        camdisp_thread = Thread(target=thread_camera_display)
        camdisp_thread.daemon=True
        camdisp_thread.start()      # Start Thread  # : cannot connect to X server

    if not DEBUG:
        app.run(host='0.0.0.0', debug=True, use_reloader=False)
    else:
        app.run(host='0.0.0.0', debug=True, use_reloader=True)
