import sys
import cv2
import os
import string
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import serial_communication as com
import pose_detection as det
import categorize as cat
import utils

class StuntsenseGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.file_counter = 6
        self.resources_path = "C:/Users/rafae/OneDrive - UGM 365/PKM/stuntsense_ws/resources/"
        self.file_name = "foto"+str(self.file_counter)+".png"

        # Layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        # Input fields
        self.mode_input = QLineEdit()
        self.mode_input.setPlaceholderText("Input Mode")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Input Name")
        self.gender_input = QLineEdit()
        self.gender_input.setPlaceholderText("Input Gender")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Input Age")

        # Add input fields to the right layout
        self.right_layout.addWidget(self.mode_input)
        self.right_layout.addWidget(self.name_input)
        self.right_layout.addWidget(self.gender_input)
        self.right_layout.addWidget(self.age_input)

        # Image label for video feed
        self.image_label = QLabel()
        self.left_layout.addWidget(self.image_label)

        # Capture and Start buttons
        self.capture_button = QPushButton('Take Picture')
        self.start_button = QPushButton('Start Process')
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        # Add buttons to the right layout
        self.right_layout.addWidget(self.capture_button)
        self.right_layout.addWidget(self.start_button)
        self.right_layout.addWidget(self.output_text)

        # Image label for result
        self.result_label = QLabel()
        self.right_layout.addWidget(self.result_label)

        # Add left and right layouts to the main layout
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)
        self.setWindowTitle('Stuntsense GUI')

        self.capture = cv2.VideoCapture(0)  # Use 0 for the default camera
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update the frame every 30 ms

        self.capture_button.clicked.connect(self.take_picture)
        self.start_button.clicked.connect(self.start_process)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            q_img = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def take_picture(self):
        ret, frame = self.capture.read()
        if ret:
            while os.path.isfile(self.resources_path + self.file_name):
                self.file_counter += 1
                self.file_name = "foto"+str(self.file_counter)+".png"
            cv2.imwrite(os.path.join(self.resources_path, self.file_name), frame)
            self.output_text.append('Picture taken and saved to folder resources!')
            
            # Output the Image
            height, width, channel = frame.shape
            step = channel * width
            q_img = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.result_label.setPixmap(QPixmap.fromImage(q_img))

    def start_process(self):
        try:
            stuntsense_com = com.SerialCommunication('COM13')
            serial_msg = stuntsense_com.read_serial()
            cam_dist = int(serial_msg[0].strip())
            cam_roll = float(serial_msg[1].strip())
            cam_pitch = float(serial_msg[2].strip())

            mode = string.capwords(self.mode_input.text())
            name = string.capwords(self.name_input.text())
            gender = string.capwords(self.gender_input.text())
            age = int(self.age_input.text())

            stuntsense_det = det.PoseDetection()
            frame = cv2.imread(self.resources_path + self.file_name)
            frame_copy = frame.copy() # for testing

            # Pose Detection
            frame = stuntsense_det.find_pose(frame, True)
            LMlist = stuntsense_det.find_position(frame, True)

            if len(LMlist) == 0:
                self.output_text.append('Cannot detect human body!')
            else:
                self.output_text.append("Pose Detected!")

            # Head Detection
            head_img = frame_copy[0:LMlist[12][2] + 5, LMlist[12][1] - 5:LMlist[11][1] + 5] # Head Cropping
            top_of_head = stuntsense_det.find_head(head_img, True)
            self.output_text.append("Head Detected!")

            # Height Measurement
            stuntsense_utils = utils.Utils()

            right_leg_pixel = stuntsense_utils.get_euclidean(LMlist[30], LMlist[28]) + stuntsense_utils.get_euclidean(LMlist[28], LMlist[26]) + stuntsense_utils.get_euclidean(LMlist[26], LMlist[24])
            left_leg_pixel = stuntsense_utils.get_euclidean(LMlist[29], LMlist[27]) + stuntsense_utils.get_euclidean(LMlist[27], LMlist[25]) + stuntsense_utils.get_euclidean(LMlist[25], LMlist[23])
            leg_pixel = (right_leg_pixel + left_leg_pixel) / 2

            right_base_pixel = stuntsense_utils.get_euclidean(LMlist[24], LMlist[12])
            left_base_pixel = stuntsense_utils.get_euclidean(LMlist[23], LMlist[11])
            base_pixel = (right_base_pixel + left_base_pixel) / 2

            neck_arr = np.array([0, (int(((LMlist[11][1]-LMlist[12][1])/2) + LMlist[12][1])), (int(((LMlist[11][2]-LMlist[12][2])/2) + LMlist[12][2]))])
            top_of_head_arr = np.array([0, (int(top_of_head.x * head_img.shape[1]) + LMlist[12][1]), int(top_of_head.y * head_img.shape[0])])
            head_pixel = stuntsense_utils.get_euclidean(neck_arr, top_of_head_arr)

            cv2.circle(frame, (top_of_head_arr[1], top_of_head_arr[2]), 3, (255,0,0), -1)
            cv2.circle(frame, (neck_arr[1], neck_arr[2]), 3, (255,0,0), -1)

            height_pixel = leg_pixel + base_pixel + head_pixel

            self.output_text.append(str(leg_pixel))
            self.output_text.append(str(base_pixel))
            self.output_text.append(str(head_pixel))
            self.output_text.append(str(height_pixel))

            height_cm = height_pixel / stuntsense_utils.pixel_per_metric()
            self.output_text.append(str(height_cm))

            # Classification
            stuntsense_cat = cat.Categorize(mode, age, gender, height_cm)
            th_list = stuntsense_cat.get_th()
            status = stuntsense_cat.get_status(th_list)

            self.output_text.append(str(th_list))
            self.output_text.append(str(status))
            
            # Output the Result Image
            height, width, channel = frame.shape
            step = channel * width
            q_img = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.result_label.setPixmap(QPixmap.fromImage(q_img))
        
        except:
            self.output_text.append('Error! Check the input then retry!')
            pass
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = StuntsenseGUI()
    gui.show()
    sys.exit(app.exec_())
