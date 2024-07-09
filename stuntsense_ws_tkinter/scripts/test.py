# import cv2 
# import detection as det

# cap = cv2.VideoCapture(0)
# stuntsense_det = det.Detection()

# while(True): 
#     ret, frame = cap.read()
#     frame_copy = frame.copy()

#     # Pose Detection
#     frame_pose = stuntsense_det.draw_pose(frame, True)
#     LMlist = stuntsense_det.get_pose_coords(frame, True)

#     # Head Detection
#     # head_img = frame_copy[0:LMlist[12][2] + 5, LMlist[12][1] - 5:LMlist[11][1] + 5] # Head Cropping
#     # top_of_head = stuntsense_det.head_detection(head_img, True)

#     if len(LMlist) == 0:
#         print('Cannot detect human body!')
#     else:
#         print("Pose Detected!")

#     cv2.imshow('frame', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'): 
#         break

# cap.release() 
# cv2.destroyAllWindows()