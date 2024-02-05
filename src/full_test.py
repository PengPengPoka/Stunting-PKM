import cv2
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import keyboard
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import string

class PoseDetector():
    def __init__(self, 
                 mode = False, 
                 complexity = 1, 
                 smooth = True, 
                 segmentation = False,
                 smoothSegmentation = True, 
                 detectCon = 0.5, 
                 trackCon = 0.5):
        
        self.static_image_mode = mode
        self.model_complexity = complexity
        self.smooth_landmarks = smooth
        self.enable_segmentation = segmentation
        self.smooth_segmentation = smoothSegmentation
        self.min_detection_confidence = detectCon
        self.min_tracking_confidence = trackCon

        self.mpPose = mp.solutions.mediapipe.solutions.pose
        self.mpDraw = mp.solutions.mediapipe.solutions.drawing_utils
        self.pose = self.mpPose.Pose(self.static_image_mode, 
                                     self.model_complexity, 
                                     self.smooth_landmarks, 
                                     self.enable_segmentation, 
                                     self.smooth_segmentation, 
                                     self.min_detection_confidence, 
                                     self.min_tracking_confidence)

    def findPose(self, img, draw = True):
        rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result = self.pose.process(rgb)
        if self.result.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.result.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        lm_list = []
        if self.result.pose_landmarks:
            for id,lm in enumerate(self.result.pose_landmarks.landmark):
                h,w,c = img.shape
                # print(id,lm)
                px, py = int(lm.x * w), int(lm.y * h)
                lm_list.append([id,px,py])
                
                if draw:
                    cv2.circle(img,(px,py),3,(255,0,0),cv2.FILLED)
        return lm_list

class category:
    def __init__(self, param, age, gender, size):
        self.param = string.capwords(param)
        self.age = int(age)
        self.gender = string.capwords(gender)
        self.size = float(size)
    
    def get_th(self):
        th_list = np.zeros(7)
        if(self.gender == "Laki-laki"):
            if(self.param == "Panjang" and self.age >=0 and self.age <=24):
                print("Penggolongan Panjang Badan Laki-laki (0-24)")
                th_list[0] = (0.0031*((self.age+1)**3)) - (0.1685*((self.age+1)**2)) + (3.7408*(self.age+1)) + 41.996
                th_list[1] = (0.0031*((self.age+1)**3)) - (0.1680*((self.age+1)**2)) + (3.7738*(self.age+1)) + 43.864
                th_list[2] = (0.0032*((self.age+1)**3)) - (0.1678*((self.age+1)**2)) + (3.8046*(self.age+1)) + 45.782
                th_list[3] = (0.0032*((self.age+1)**3)) - (0.1678*((self.age+1)**2)) + (3.8395*(self.age+1)) + 47.651
                th_list[4] = (0.0032*((self.age+1)**3)) - (0.1674*((self.age+1)**2)) + (3.8701*(self.age+1)) + 49.566
                th_list[5] = (0.0029*((self.age+1)**3)) - (0.1582*((self.age+1)**2)) + (3.8297*(self.age+1)) + 51.565
                th_list[6] = (0.0032*((self.age+1)**3)) - (0.1659*((self.age+1)**2)) + (3.9249*(self.age+1)) + 53.358
            elif(self.param == "Tinggi" and self.age >=24 and self.age <= 60):
                print("Penggolongan Tinggi Badan Laki-laki (24-60)")
                th_list[0] = (0.4932*(self.age-24)) + 78.265
                th_list[1] = (0.5361*(self.age-24)) + 81.368
                th_list[2] = (0.5784*(self.age-24)) + 84.491
                th_list[3] = (0.6213*(self.age-24)) + 87.597
                th_list[4] = (0.6634*(self.age-24)) + 90.717
                th_list[5] = (0.7063*(self.age-24)) + 93.826
                th_list[6] = (0.7500*(self.age-24)) + 96.918
        
        elif(self.gender == "Perempuan"):
            if(self.param == "Panjang" and self.age >=0 and self.age <=24):
                print("Penggolongan Panjang Badan Perempuan (0-24)")
                th_list[0] = (0.0026*((self.age+1)**3)) - (0.1390*((self.age+1)**2)) + (3.2942*(self.age+1)) + 41.667
                th_list[1] = (0.0026*((self.age+1)**3)) - (0.1415*((self.age+1)**2)) + (3.3779*(self.age+1)) + 43.453
                th_list[2] = (0.0026*((self.age+1)**3)) - (0.1422*((self.age+1)**2)) + (3.4457*(self.age+1)) + 45.262
                th_list[3] = (0.0027*((self.age+1)**3)) - (0.1430*((self.age+1)**2)) + (3.5099*(self.age+1)) + 47.099
                th_list[4] = (0.0027*((self.age+1)**3)) - (0.1451*((self.age+1)**2)) + (3.5895*(self.age+1)) + 48.898
                th_list[5] = (0.0028*((self.age+1)**3)) - (0.1471*((self.age+1)**2)) + (3.6650*(self.age+1)) + 50.724
                th_list[6] = (0.0028*((self.age+1)**3)) - (0.1481*((self.age+1)**2)) + (3.7327*(self.age+1)) + 52.533
                
            elif(self.param == "Tinggi" and self.age >=24 and self.age <= 60):
                print("Penggolongan Tinggi Badan Perempuan (24-60)")
                th_list[0] = (0.5237*(self.age-24)) + 76.477
                th_list[1] = (0.5664*(self.age-24)) + 79.696
                th_list[2] = (0.6087*(self.age-24)) + 82.945
                th_list[3] = (0.6502*(self.age-24)) + 86.181
                th_list[4] = (0.6922*(self.age-24)) + 89.431
                th_list[5] = (0.7340*(self.age-24)) + 92.673
                th_list[6] = (0.7770*(self.age-24)) + 95.896

        return th_list

    def get_status(self, th_list):
        if(self.size<th_list[0]):
            status = "severely_stunted"
        elif(self.size>=th_list[0] and self.size<th_list[1]):
            status = "stunted"
        elif(self.size>=th_list[1] and self.size<=th_list[6]):
            status = "normal"
        elif(self.size>th_list[6]):
            status = "tinggi"

        return status

def measurement(array1, array2):
    euclidean_distance = np.sqrt(((array2[1] - array1[1]) ** 2) + ((array2[2] - array1[2]) ** 2))

    return euclidean_distance

def pixel_per_metric(dimension):
    constant_length = 4
    ppm = dimension / constant_length
    return ppm

def main():
    # Input Data
    mode = input("Masukkan mode: ")
    gender = input("Masukkan jenis kelamin: ")
    age = input("Masukkan umur: ")

    # Just Def
    first_detector = PoseDetector()
    sec_detector = PoseDetector()

    counter = 0
    key_pressed = 0
    # resource_path = "C:/Users/rafae/Documents/Stunting-PKM/resources/"
    # file_name = "foto"+str(counter)+".png"

    cap = cv2.VideoCapture(0)
    prev_time = 0

    # # Camera Processing
    # while True:
    #     ret, frame = cap.read()

    #     # FPS Calculation
    #     cur_time = time.time()
    #     fps = 1/(cur_time-prev_time)
    #     prev_time = cur_time
    #     cv2.putText(frame,str(int(fps)),(30,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    #     # Take a Pict
    #     if keyboard.is_pressed('p') and key_pressed == 0:
    #         key_pressed = 1
    #         while os.path.isfile(resource_path + file_name):
    #             counter += 1
    #             file_name = "foto"+str(counter)+".png"
    #         cv2.imwrite(os.path.join(resource_path, file_name), frame)
    #     elif keyboard.is_pressed('p') == 0:
    #         key_pressed = 0
        
    #     if keyboard.is_pressed('q'):
    #         break
        
    #     cv2.imshow("video",frame)
    #     cv2.waitKey(30)

    # Frame to Process
    # frame = cv2.imread(resource_path + file_name)
    frame = cv2.imread("D:/Proyek/Stunting-PKM/resources/foto0.png")
    # frame = cv2.resize(frame, (640,480))

    # Resize to Simplify (not used)
    # if(frame.shape[0] < frame.shape[1]):
    #     frame = cv2.resize(frame, (640, 480))
    # else:
    #     frame = cv2.resize(frame, (480, 640))

    # Make a Copy
    frame_temp = frame.copy() # for testing

    # Orientation Check
    frame_temp = first_detector.findPose(frame_temp,True)
    LMlist_cpy = first_detector.findPosition(frame_temp,True)

    if len(LMlist_cpy) == 0:
        print("Nothing")
    else:
        shoulder_x = LMlist_cpy[11][1] - LMlist_cpy[12][1]
        shoulder_y = LMlist_cpy[11][2] - LMlist_cpy[12][2]
        nose_y = LMlist_cpy[0][2]

    if(np.fabs(shoulder_x) < np.fabs(shoulder_y)):
        if(shoulder_y > 0):
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif(nose_y - LMlist_cpy[11][2] > 0):
        frame = cv2.rotate(frame, cv2.ROTATE_180)

    frame_new = frame.copy() # store original frame on right orientation
    
    # Pose Detection
    frame = sec_detector.findPose(frame,True)
    LMlist = sec_detector.findPosition(frame,True)

    if len(LMlist) == 0:
        print("Nothing")
    else:
        print("Pose Detected!")

    # Head Cropping
    frame_temp = frame_new[0:LMlist[12][2] + 5, LMlist[12][1] - 5:LMlist[11][1] + 5]
    rgb = cv2.cvtColor(frame_temp, cv2.COLOR_BGR2RGB)
    
    # Face Mesh
    head_x = head_y = neck_x = neck_y = 0
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2, min_detection_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    face_mesh_results = face_mesh_images.process(rgb[:,:,::-1])

    if face_mesh_results.multi_face_landmarks:
        for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
            pt1 = face_landmarks.landmark[10]
            head_x = int(pt1.x * frame_temp.shape[1]) + LMlist[12][1]
            head_y = int(pt1.y * frame_temp.shape[0])
            cv2.circle(frame, (head_x, head_y), 3, (255,0,0), -1)
            neck_x = (int)(((LMlist[11][1]-LMlist[12][1])/2) + LMlist[12][1])
            neck_y = (int)((LMlist[11][2]-LMlist[12][2])/2) + LMlist[12][2]
            cv2.circle(frame, (neck_x, neck_y), 3, (255,0,0), -1)
    else:
        print("Nothing")

    # Height Measurement
    print(LMlist[30], LMlist[28], LMlist[26], LMlist[24])
    print(LMlist[29], LMlist[27], LMlist[25], LMlist[23])
    r_leg = measurement(LMlist[30], LMlist[28]) + measurement(LMlist[28], LMlist[26]) + measurement(LMlist[26], LMlist[24])
    l_leg = measurement(LMlist[29], LMlist[27]) + measurement(LMlist[27], LMlist[25]) + measurement(LMlist[25], LMlist[23])
    leg = (r_leg + l_leg) / 2
    interpupillary_dist = measurement(LMlist[2],LMlist[5])
    print("LEG: ", leg)

    r_base = measurement(LMlist[24], LMlist[12])
    l_base = measurement(LMlist[23], LMlist[11])
    base = (r_base + l_base) / 2
    print("BASE: ", base)
    
    arr_neck = np.array([0, neck_x, neck_y])
    arr_head = np.array([0, head_x, head_y])
    head = measurement(arr_neck, arr_head)
    print("HEAD: ", head)

    total_height = leg + base + head
    print("HEIGHT: ", total_height)

    print("INTERPUPILLARY DISTANCE: ", interpupillary_dist)

    ppm = pixel_per_metric(interpupillary_dist)
    print("PPM: ", ppm)

    real_height = total_height / ppm
    print("REAL HEIGHT: {} cm".format(real_height))

    # Classification
    p = category(mode, age, gender, real_height)
    th_list = p.get_th()
    print("Standar Deviasi: ", th_list)
    status = p.get_status(th_list)
    print("Status: ", status)
    
    cv2.imshow("result", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows

if __name__ == "__main__":
    main()