import sys
import cv2
import os
import string
import numpy as np
import csv
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import serial_communication as com
import detection as det
import categorize as cat
import utils

class TkInterGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.file_counter = 34
        self.resources_path = "C:/Users/rafae/Downloads/stuntsense_ws/resources/"
        self.file_name = "foto"+str(self.file_counter)+".png"

        self.title('Stuntsense GUI')
        
        # Main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for video feed
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.image_label = ttk.Label(self.left_frame)
        self.image_label.pack()

        # Right frame for input and buttons
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.mode_input = ttk.Entry(self.right_frame)
        self.mode_input.insert(0, "Input Mode")
        self.mode_input.pack(pady=5)

        self.name_input = ttk.Entry(self.right_frame)
        self.name_input.insert(0, "Input Name")
        self.name_input.pack(pady=5)

        self.gender_input = ttk.Entry(self.right_frame)
        self.gender_input.insert(0, "Input Gender")
        self.gender_input.pack(pady=5)

        self.age_input = ttk.Entry(self.right_frame)
        self.age_input.insert(0, "Input Age")
        self.age_input.pack(pady=5)

        self.capture_button = ttk.Button(self.right_frame, text='Take Picture', command=self.take_picture)
        self.capture_button.pack(pady=5)

        self.start_button = ttk.Button(self.right_frame, text='Start Process', command=self.start_process)
        self.start_button.pack(pady=5)

        self.output_text = tk.Text(self.right_frame, state='disabled', height=10)
        self.output_text.pack(pady=5)

        self.result_label = ttk.Label(self.right_frame)
        self.result_label.pack()

        self.capture = cv2.VideoCapture(0)  # Use 0 for the default camera
        self.update_frame()

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = frame.shape
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)
        self.after(30, self.update_frame)

    def take_picture(self):
        ret, frame = self.capture.read()
        if ret:
            while os.path.isfile(self.resources_path + self.file_name):
                self.file_counter += 1
                self.file_name = "foto"+str(self.file_counter)+".png"
            cv2.imwrite(os.path.join(self.resources_path, self.file_name), frame)
            self.output_text.config(state='normal')
            self.output_text.insert(tk.END, 'Picture taken and saved to folder resources!\n')
            
            # Output the Image
            height, width, _ = frame.shape
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.result_label.imgtk = imgtk
            self.result_label.configure(image=imgtk)

            # Read Sensor
            # stuntsense_com = com.SerialCommunication('/dev/ttyACM0')
            # serial_msg = stuntsense_com.read_serial()
            # self.cam_dist = int(serial_msg[0].strip())
            # self.cam_roll = float(serial_msg[1].strip())
            # self.cam_pitch = float(serial_msg[2].strip())

            self.output_text.insert(tk.END, str("Distance: "))
            self.output_text.insert(tk.END, str(self.cam_dist) + "\n")
            self.output_text.insert(tk.END, str("Roll Angle: "))
            self.output_text.insert(tk.END, str(self.cam_roll) + "\n")
            self.output_text.insert(tk.END, str("Pitch Angle: "))
            self.output_text.insert(tk.END, str(self.cam_pitch) + "\n")
            self.output_text.config(state='disabled')

    def start_process(self):
        try:
            self.output_text.config(state='normal')

            self.cam_dist = 228
            self.cam_roll = -72.2
            self.cam_pitch = -4.0

            # Get Input Data
            mode = string.capwords(self.mode_input.get())
            name = string.capwords(self.name_input.get())
            gender = string.capwords(self.gender_input.get())
            age = int(self.age_input.get())

            stuntsense_det = det.Detection()
            frame = cv2.imread(self.resources_path + self.file_name)
            frame_copy = frame.copy() # for testing

            # Pose Detection
            frame = stuntsense_det.draw_pose(frame, True)
            LMlist = stuntsense_det.get_pose_coords(frame, True)

            if len(LMlist) == 0:
                self.output_text.insert(tk.END, 'Cannot detect human body!\n')
            else:
                self.output_text.insert(tk.END, "Pose Detected!\n")

            # Head Detection
            head_img = frame_copy[0:LMlist[12][2] + 5, LMlist[12][1] - 5:LMlist[11][1] + 5] # Head Cropping
            top_of_head = stuntsense_det.head_detection(head_img, True)
            self.output_text.insert(tk.END, "Head Detected!\n")

            # Height Measurement
            stuntsense_utils = utils.Utils()

            right_leg_pixel = stuntsense_utils.get_euclidean_dist(LMlist[30], LMlist[28]) + stuntsense_utils.get_euclidean_dist(LMlist[28], LMlist[26]) + stuntsense_utils.get_euclidean_dist(LMlist[26], LMlist[24])
            left_leg_pixel = stuntsense_utils.get_euclidean_dist(LMlist[29], LMlist[27]) + stuntsense_utils.get_euclidean_dist(LMlist[27], LMlist[25]) + stuntsense_utils.get_euclidean_dist(LMlist[25], LMlist[23])
            leg_pixel = (right_leg_pixel + left_leg_pixel) / 2

            right_base_pixel = stuntsense_utils.get_euclidean_dist(LMlist[24], LMlist[12])
            left_base_pixel = stuntsense_utils.get_euclidean_dist(LMlist[23], LMlist[11])
            base_pixel = (right_base_pixel + left_base_pixel) / 2

            neck_arr = np.array([0, (int(((LMlist[11][1]-LMlist[12][1])/2) + LMlist[12][1])), (int(((LMlist[11][2]-LMlist[12][2])/2) + LMlist[12][2]))])
            top_of_head_arr = np.array([0, (int(top_of_head.x * head_img.shape[1]) + LMlist[12][1]), int(top_of_head.y * head_img.shape[0])])
            head_pixel = stuntsense_utils.get_euclidean_dist(neck_arr, top_of_head_arr)

            cv2.circle(frame, (top_of_head_arr[1], top_of_head_arr[2]), 3, (255,0,0), -1)
            cv2.circle(frame, (neck_arr[1], neck_arr[2]), 3, (255,0,0), -1)

            height_pixel = leg_pixel + base_pixel + head_pixel
            height_cm = (height_pixel / frame.shape[0]) * stuntsense_utils.convert_to_cm(self.cam_dist)

            # Classification
            stuntsense_cat = cat.Categorize(mode, age, gender, height_cm)
            th_list = stuntsense_cat.get_th()
            status = stuntsense_cat.get_status(th_list)

            # Print the Results
            self.output_text.insert(tk.END, str("PXL: "))
            self.output_text.insert(tk.END, str(height_pixel) + "\n")
            self.output_text.insert(tk.END, str("CM: "))
            self.output_text.insert(tk.END, str(height_cm) + "\n")
            self.output_text.insert(tk.END, str("SD Value: "))
            self.output_text.insert(tk.END, str(th_list) + "\n")
            self.output_text.insert(tk.END, str("Stunting Status: "))
            self.output_text.insert(tk.END, str(status) + "\n")

            # Print to CSV
            csv_file = '/home/rafael/stuntsense_ws/results/data_log.csv'
            header = ['Name', 'File name', 'Distance', 'Roll Angle', 'Pitch Angle', 'Height_Pixel', 'Height_CM', 'Status']

            try:
                with open(csv_file, mode='r') as file:
                    pass
            except FileNotFoundError:
                with open(csv_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)

            file_name = self.resources_path + self.file_name
            data = [name, file_name, self.cam_dist, self.cam_roll, self.cam_pitch, height_pixel, height_cm, status]

            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)

            self.output_text.insert(tk.END, str("Data stored to CSV file successfully.\n"))
            self.output_text.insert(tk.END, str("--------------------------------------------------------------------\n"))
            self.output_text.config(state='disabled')
            
            # Output the Result Image
            height, width, _ = frame.shape
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.result_label.imgtk = imgtk
            self.result_label.configure(image=imgtk)
        
        except Exception as e:
            self.output_text.config(state='normal')
            self.output_text.insert(tk.END, f'Error! Check the input then retry! {str(e)}\n')
            self.output_text.config(state='disabled')
            pass

if __name__ == '__main__':
    gui = TkInterGUI()
    gui.mainloop()
