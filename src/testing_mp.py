import cv2 as cv
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import numpy as np
import matplotlib.pyplot as plt

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
        rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
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
                    cv.circle(img,(px,py),3,(255,0,0),cv.FILLED)
        return lm_list


def main():
    detector = PoseDetector()

    # cap = cv.VideoCapture(1)
    pTime = 0

    frame = cv.imread("C:/Users/rafae/OneDrive/Documents/learn_opencv/resources/bayi.png")
    frame = cv.resize(frame, (640, 480))
    frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    frame_cpy = frame.copy()

    print(frame.shape)

    # while True:
    # grab, frame = cap.read()

    # if not grab:
    #     print("no video avaiable")

    # frame = cv.resize(frame,(800,500))
    frame = detector.findPose(frame,True)
    LMlist = detector.findPosition(frame,True)
    

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(frame,str(int(fps)),(30,50),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    
    if len(LMlist) == 0:
        print("list is empty")
    else:
        print(LMlist[12])

    frame_cpy = frame_cpy[0:LMlist[12][2], LMlist[12][1]:LMlist[11][1]]
    rgb = cv.cvtColor(frame_cpy, cv.COLOR_BGR2RGB)

    # Face Mesh
    mp_face_mesh = mp.solutions.face_mesh

    face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2,
                                            min_detection_confidence=0.5)

    mp_drawing = mp.solutions.drawing_utils

    mp_drawing_styles = mp.solutions.drawing_styles

    face_mesh_results = face_mesh_images.process(rgb[:,:,::-1])

    if face_mesh_results.multi_face_landmarks:
        for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
            # print(face_landmarks.landmark[10])
            pt1 = face_landmarks.landmark[10]
            x = int(pt1.x * frame_cpy.shape[1]) + LMlist[12][1]
            y = int(pt1.y * frame_cpy.shape[0])
            print("x", x, "y", y)
            cv.circle(frame, (x,y), 3, (255,0,0), -1)
            leher_x = (int)(((LMlist[11][1]-LMlist[12][1])/2)  + LMlist[12][1])
            cv.circle(frame, (leher_x,LMlist[12][2]), 3, (255,0,0), -1)
    else:
        print("Nothing")

    
    cv.imshow("rgb",rgb)
    cv.imshow("crop", frame_cpy)
    cv.imshow("result",frame)

    cv.waitKey(0)
    cv.destroyAllWindows


if __name__ == "__main__":
    main()