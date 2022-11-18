import face_recognition
import cv2
import os

import time

class CFaceRecWebcam:
    def __init__(self):
    
        self.init()
    def init(self):
        # This is a super simple (but slow) example of running face recognition on live video from your webcam.
        # There's a second example that's a little more complicated but runs faster.

        # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
        # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
        # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
        print("이미지 학습...")
        # Get a reference to webcam #0 (the default one)
        #self.video_capture = cv2.VideoCapture(0)

        # Load a sample picture and learn how to recognize it.
        # obama_image = face_recognition.load_image_file("./resource/customer/obama.jpg")
        # print (obama_image.shape)
        #face_recognition.face_landmarks("shape_predictor_68_face_landmarks.dat")


        self.known_face_encodings = []
        self.known_face_names = []

        img_list = self.GetAllImageFileName()
        print("img_list", img_list)
        
        #exit()


        for img in img_list:
            print(img)
            #image = face_recognition.load_image_file("./resource/customer/%s"%img)
            
            image = face_recognition.load_image_file("/home/pi/Pictures/%s"%img)
            #print(image)
            encoding = face_recognition.face_encodings(image)[0]
            self.known_face_encodings.append(encoding)

            id = img.split(".")
            self.known_face_names.append(id[0])


        """
        obama_image = face_recognition.load_image_file("./resource/customer/seo_resize.jpg")
        print (obama_image.shape)

        


        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("./resource/customer/biden.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        
        # Create arrays of known face encodings and their names
        self.known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding
        ]
        self.known_face_names = [
            "ID00000002",
            "Joe Biden"
        ]

        """


    def GetAllImageFileName(self):
        #workDIr = os.path.abspath('./resource/customer')
        workDIr = os.path.abspath('/home/pi/Pictures')
        
        filenames = []
        for dirpath, dirnames, filenames in os.walk(workDIr):
            print (dirpath)

            for dirname in dirnames:
                print ("\t", dirname)

            for filename in filenames:
                print ("\t", filename)
        
        
        return filenames
        
        if len(filename) == 0:
            return []
        elif len(filename) == 1:
            return [filenames]
        else:
            return filenames



    def FaceRecognition_fast_alone_ex(self):
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []


        # time.sleep(5)
        while True:
            count += 1
            # print("grab frame: ", count)

            # Grab a single frame of video
            ret, frame = self.video_capture.read()


            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            cv2.imshow('Video', rgb_small_frame)

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.known_face_names[first_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame
            # print("face_names ", face_names) # face_names  ['Unknown'],  face_names  ['ID00000002']

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)



            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if face_names:
                print("found face ", face_names)
                break
            if time.time() - start_time > 5:
                print("not found face")
                break




        # Release handle to the webcam

        time.sleep(2)
        self.video_capture.release()
        cv2.destroyAllWindows()
        # print ()
        return face_names


    def FaceRecognitionFromFrame(self, frame):
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        name = ""


        # while True:
        # Grab a single frame of video
        # ret, frame = self.video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        top = 0
        right = 0
        bottom = 0
        left = 0
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            if name == "Unknown":
                color = (255,0,0)
            else:
                color = (0,0,255)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return name, frame, top, right, bottom, left
        # Display the resulting image
        # cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        # k=cv2.waitKey(30)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        # Release handle to the webcam
        # self.video_capture.release()
        # cv2.destroyAllWindows()




    def FaceRecognition(self):
        while(True):
            # Grab a single frame of video
            ret, frame = self.video_capture.read()

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces and face enqcodings in the frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Loop through each face in this frame of video
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        self.video_capture.release()
        cv2.destroyAllWindows()



    def remove_image(self, id):
        filename = "/home/pi/Pictures/%s.jpg"%id
        os.remove(filename)

    def remove_image_all(self):
        img_list = self.GetAllImageFileName()
        for img in img_list:
            os.remove("/home/pi/Pictures/"+img)
    

    def resize_image(self, id):
        # read the image
        filename = "/home/pi/Pictures/%s.jpg"%id
        image = cv2.imread(filename)

        print("Original shape: ", image.shape)

        height = image.shape[0]
        width = image.shape[1]

        # let's say we want the new width to be 400px
        # and compute the new height based on the aspect ratio
        new_width = 200
        ratio = new_width / width # (or new_height / height)
        new_height = int(height * ratio)

        dimensions = (new_width, new_height)
        new_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_LINEAR)

        print("New shape:      ", new_image.shape)

        #cv2.imshow("Original image", image)
        #cv2.imshow("Resized image", new_image)

        cv2.imwrite(filename, new_image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        



    # face_names = obj.FaceRecognition_fast_alone_ex()
