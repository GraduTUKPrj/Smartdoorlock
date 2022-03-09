import dlib
import cv2
import numpy as np
import time
import socket
import os

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:\RPi4\Project\shape_predictor_68_face_landmarks.dat")
face_recog = dlib.face_recognition_model_v1("C:\RPi4\Project\dlib_face_recognition_resnet_model_v1.dat")

# 인코딩 데이터 불러오기

descs = np.load('C:\RPi4\Project\desc\a20_descs.npy', allow_pickle=True)[()]


# 들어온 영상에서 이미지 찾기
def encode_faces(image):
    faces = detector(image, 1)

    if len(faces) == 0:
        return np.empty(0)

    for k, d in enumerate(faces):
        land = predictor(image, d)
        face_decriptor = face_recog.compute_face_descriptor(image, land)

        return np.array(face_decriptor)


stream_cap = cv2.VideoCapture(0)
time.sleep(0.1)






# check the image + 저장name
checks = 0
check_sum = 0
save_ph = ""

while True:
    ret, img_bgr = stream_cap.read()

    if not ret:
        break

    img_rgb = cv2.cvtcolor(img_bgr, cv2.color_bgr2rgb)

    faces = detector(img_rgb, 1)

    for k, d in enumerate(faces):
        # 사각형위치 찾아놓기
        rect = ((d.left(), d.top()), (d.right(), d.bottom()))

        land = predictor(img_rgb, d)
        face_descriptor = face_recog.compute_face_descriptor(img_rgb, land)

        last_found = {'name': 'unknown', 'dist': 0.6, 'color': (0, 0, 255)}

        for name, saved_desc in descs.items():
            dist = np.linalg.norm([face_descriptor] - saved_desc, axis=1)

            if dist < last_found['dist']:
                last_found = {'name': name, 'dist': dist, 'color': (255, 255, 255)}

        cv2.rectangle(img_bgr, pt1=(d.left(), d.top()), pt2=(d.right(), d.bottom()), color=last_found['color'],
                      thickness=2)
        cv2.puttext(img_bgr, last_found['name'], org=(d.left(), d.top()), fontface=cv2.font_hershey_simplex,
                    fontscale=1, color=last_found['color'], thickness=2)
        # print('  :  ' + last_found['name'])
        print('name :  ', last_found['name'])
        print("오차 : ", dist)

        # 연속으로 동작 확인
        if (checks == 0):
            first_name = last_found['name']

        if (check_sum < 4):
            if (first_name == last_found['name']):
                check_sum += 1
                checks += 1
            else:
                checks = 0
                check_sum = 0





    cv2.imshow('face_recognation', img_bgr)
    if cv2.waitkey(1) == ord('q'):
        break

stream_cap.release()
cv2.destroyAllWindows()
