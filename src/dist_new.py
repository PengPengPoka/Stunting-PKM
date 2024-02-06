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

def measurement(array1, array2):
    euclidean_distance = np.sqrt(((array2[1] - array1[1]) ** 2) + ((array2[2] - array1[2]) ** 2))

    return euclidean_distance

def pixel_per_metric(dimension):
    constant_length = 4
    ppm = dimension / constant_length
    return ppm

def main():
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
    frame = cv2.imread("D:/Proyek/Stunting-PKM/data/test_results/test_107/test_img.jpg")
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
            head_y = int(pt1.y * frame_temp.shape[0]) - 50
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
    print("REAL HEIGHT: {:.2f} cm".format(real_height))


    
    cv2.imshow("result", frame)

    cv2.waitKey(0)
    cv2.destroyAllWindows

if __name__ == "__main__":
    main()


