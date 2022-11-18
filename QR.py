#-*- coding:utf-8 -*-

import os, time

import numpy as np


class CQrCode:
    def __init__(self):
        print("Start :", str(self))

    def __del__(self):
        pass


    # QR코드 생성 예제 테스트용 함수
    def TEST_QrCodeGen(self, data):
    
        """
        #https://blog.naver.com/chandong83/221767329995
        > pip install qrcode[pil]
        or
        > pip install qrcode pillow  # rpi에서 이거로 설치함
        """

        import qrcode

        # Hello World! 로 QR 코드 생성
        img = qrcode.make(data)

        # 생성된 이미지를 helloworld_qrcode.png로 저장
        # img.save('/home/pi/capture_save/phone_%s.png'%phonenumber)  # rpi에서 동작확인함
        if os.name == 'nt':
            img.save('%s.png'%data)
        else:
            img.save('/home/pi/capture_save/qrpassword.png')
    
    # QR코드 읽기 예제(이미지 파일로 읽기)
    def TEST_QrCodeScan(self):
            
        #pip3 install pyzbar
        import pyzbar.pyzbar as pyzbar
        import cv2
        import imutils

        img=cv2.imread("cam_qr_name4.jpg", 1)
        #img=cv2.imread("cam_crop.jpg", 1) 
        img = imutils.resize(img, width=450) # debug
        result = self.DetectQrcode(img)
        if result == "":
            print ("QR is not Detected")
        
        else:
            #print(result)      #('Hello World!', 40, 40, 210, 210)
            (result_text, x, y, w, h, polygon) = result
            print(result_text)  # 'Hello World!'
            print(x,y,w,h)      # '40 40 210 210'
            print(polygon)      # [Point(x=547, y=424), Point(x=559, y=885), Point(x=1087, y=839), Point(x=1043, y=388)] 좌상, 좌하, 우하, 우상






    # QR코드 검출 : image frame
    def DetectQrcode(self, frame):
        
        import pyzbar.pyzbar as pyzbar #pip3 install pyzbar
        import cv2
    
        ret_str = ""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        decoded = pyzbar.decode(gray)

        for d in decoded:
            x, y, w, h = d.rect
            print(d.polygon)
            #print(x, y, w, h)

            barcode_data = d.data.decode("utf-8")
            barcode_type = d.type

            ret_str = barcode_data
        
            return ret_str, x, y, w, h, d.polygon
        return ""


    # QR코드 검출 : camera에서 QR코드 검출
    def DetectQrcodeFromCam(self, timeout=20):
        
        import pyzbar.pyzbar as pyzbar 
        import cv2
        import time
        
        self.video_capture = cv2.VideoCapture(0)
        
        start_time = time.time()
        while True:
            ret, frame = self.video_capture.read()

      
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)


        
            ret_str = ""
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            decoded = pyzbar.decode(gray)

            for d in decoded:
                x, y, w, h = d.rect
                print(d.polygon)
                #print(x, y, w, h)

                barcode_data = d.data.decode("utf-8")
                barcode_type = d.type

                ret_str = barcode_data
            
                return ret_str, x, y, w, h, d.polygon
            
            if time.time() - start_time > timeout:
                print("timeout, can't detect qrcode")
                return ""



if __name__ == "__main__":

    try:
        #while(True):
        


        
        
        
