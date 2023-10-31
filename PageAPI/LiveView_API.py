import cv2
import os
from PyQt5.QtCore import QTimer
from Detection.Defect import (
    defect_detection,
    function_total_complete_defects_cnts,
    function_return_total_depth,
    function_return_critical_flage,
    getDate,
)
from Detection.defectTrackerClass import defectTracker

import cv2
from backend.Camera import dorsaPylon
from backend.Camera.dorsaPylon import Collector, Camera
from backend import camera_connection

class LiveView_API:

    """Description of the code

    :param
    """

    def __init__(self, ui,db_Report):
        self.ui_live = ui
        self.step = 2
        self.pix_mm_depth = 0.34
        self.pix_mm_width = 140 / 590
        self.CONVAYER_SPEED = 120  # mm/s
        self.pix_mm_length = self.step * self.CONVAYER_SPEED / 750
        self.frame_idx = 0
        self.db_Report=db_Report
        self.defect_tracker = defectTracker(min_g_thresh=20, step_per_line=2, db_Report=self.db_Report)
        self.parms_camera_liveView = {
            "Serial": 0,
            "Gain": 0,
            "Exposure": 0,
            "Width": 0,
            "Height": 0,
            "offsetX": 0,
            "offsetY": 0,
        }
        self.parms_calibration_liveView = {
            "GRADIENT_SIZE": 0,
            "MAX_ERROR": 0,
            "TEAR_DEPTH": 0,
            "Critical_Depth": 0,
        }
        self.collector = Collector()
                 
        ###################  self.camera = self.collector.get_camera_by_serial(str(self.parms_camera_liveView["Serial"]))
        self.camera = self.collector.get_camera_by_serial(str(23287291))    ###################  for getting image from  camera
        self.camera.build_converter(pixel_type=dorsaPylon.PixelType.GRAY8)         ###################  for getting image from  camera
       
        #self.cam = camera_connection.Collector(
       #     str(23287291), 217, 5000, 640, 480, 16, 16
        #)
        #self.result1, _ = self.cam.start_grabbing()
        self.button_connector()
        self.button_connector_QTimer()    ###################  for getting image from  camera

    def button_connector(self):
        self.ui_live.button_connector()    ############## for getting image from camera
        ########self.ui_live.button_connector(self.start_selection)  # for getting image from folder

    def button_connector_QTimer(
        self,
    ):  ###################  for getting image from camera
        self.ui_live.button_connector_QTimer(self.start_selection_camera)

    def start_selection(self):
        self.show_farme()

    def start_selection_camera(self):
        # self.picktimer = QTimer()
        # self.picktimer.timeout.connect(self.show_farme_camera)
        # self.picktimer.start()
        self.show_farme_camera()

    def show_image(self, frame):
        img = frame
        img = cv2.resize(
            img,
            (1000, 280),  # this is relative to the camera
            interpolation=cv2.INTER_AREA,
        )

        try:
            h, w, ch = img.shape

        except:
            h, w = img.shape

            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            ch = 3
        bytes_per_line = ch * w
        self.ui_live.set_Pixmap(img.data, w, h, bytes_per_line)

    def show_farme_camera(self):  ###################  for getting image from  camera
        self.ui_live.disable_live()
        self.camera.Operations.start_grabbing()
        img = self.camera.getPictures()
        ###########res,img = self.cam.getPictures()
        idx=self.parms_camera_liveView["Exposure"]
        #print(img.shape)
        self.frame_idx = self.frame_idx + 1
        res_img, s, Number_Defect, Number_of_Critical_Defect = defect_detection(
            self.frame_idx, img,idx,self.defect_tracker
        )
        styles_Live = {
                "Not_Critical_live_view": "background-color:rgb(219, 219, 219)",
                "Critical_live_view": "background-color:rgb(219, 219, 219) ",
                "Normal_live_view": "background-color:rgb(47, 140, 68)",
            }
        self.ui_live.set_style_information(styles_Live)


        if s != None:
                infoes_Live = {
                        "Length": "{:.2f}".format(float(s[3] * self.pix_mm_length))
                        + " "
                        + "mm",
                        "Width": "{:.2f}".format(float(s[2] * self.pix_mm_width))
                        + " "
                        + "mm",
                        "Depth": "{:.2f}".format(float(s[4])) + " " + "mm",
                        #"Depth": "{:.2f}".format(float(max_depth)) + " " + "mm",
                        "Total_Number_Defect": str(Number_Defect),
                        "Total_Number_Critical_defect": str(Number_of_Critical_Defect),
                    }
                self.ui_live.set_general_information(infoes_Live)
                #print(max_depth)
                if float(s[4]) > 20:
                        styles_Live = {
                            "Not_Critical_live_view": "background-color:rgb(219, 219, 219)",
                            "Critical_live_view": "background-color:rgb(218, 0, 0) ",
                            "Normal_live_view": "background-color:rgb(219, 219, 219)",
                        }
                        self.ui_live.set_style_information(styles_Live)

                else:
                        styles_Live = {
                            "Not_Critical_live_view": "background-color:rgb(213, 213, 0)",
                            "Critical_live_view": "background-color:rgb(219, 219, 219) ",
                            "Normal_live_view": "background-color:rgb(219, 219, 219)",
                        }
                        self.ui_live.set_style_information(styles_Live)



        self.show_image(res_img)

    def set_initial_param_calibration(self, param_cal):      
        self.set_calibration_parms_API(param_cal)


    def set_param_calibration(self, param_cal):   
        self.set_calibration_parms_API(param_cal)


    def set_initial_param_camera(self, param_cam):   
        self.set_camera_parms_API(param_cam)


    def set_param_camera(self, param_cam):  
       self.set_camera_parms_API(param_cam)


    def set_calibration_parms_API(self, example_dict): 
        for name, value in example_dict.items():
            self.parms_calibration_liveView[name]=example_dict[name]
       
    def set_camera_parms_API(self, example_dict):   
        for name, value in example_dict.items():
            self.parms_camera_liveView[name]=example_dict[name]

        ###################   self.camera.Parms.set_exposureTime(self.parms_camera_liveView["Exposure"])     ###################  for getting image from  camera
        ###############      self.camera.Parms.set_gain(self.parms_camera_liveView["Gain"])                    ###################  for getting image from  camera
         

    def show_farme(self):  ###################  for getting image from folder
        self.ui_live.disable_live()
        idx=self.parms_camera_liveView["Exposure"]
        image_path = "Part6"
       
        for frame_idx, fname in enumerate(os.listdir(image_path)):
            res_img, s, Number_Defect, Number_of_Critical_Defect,max_depth = defect_detection(
                frame_idx, fname,idx,self.defect_tracker
            )
            #print(max_depth)
            styles_Live = {
                "Not_Critical_live_view": "background-color:rgb(219, 219, 219)",
                "Critical_live_view": "background-color:rgb(219, 219, 219) ",
                "Normal_live_view": "background-color:rgb(47, 140, 68)",
            }
            self.ui_live.set_style_information(styles_Live)

            if s != None:
                infoes_Live = {
                        "Length": "{:.2f}".format(float(s[3] * self.pix_mm_length))
                        + " "
                        + "mm",
                        "Width": "{:.2f}".format(float(s[2] * self.pix_mm_width))
                        + " "
                        + "mm",
                        "Depth": "{:.2f}".format(float(s[4])) + " " + "mm",
                        #"Depth": "{:.2f}".format(float(max_depth)) + " " + "mm",
                        "Total_Number_Defect": str(Number_Defect),
                        "Total_Number_Critical_defect": str(Number_of_Critical_Defect),
                    }
                self.ui_live.set_general_information(infoes_Live)
                #print(max_depth)
                if float(s[4]) > 20:
                        styles_Live = {
                            "Not_Critical_live_view": "background-color:rgb(219, 219, 219)",
                            "Critical_live_view": "background-color:rgb(218, 0, 0) ",
                            "Normal_live_view": "background-color:rgb(219, 219, 219)",
                        }
                        self.ui_live.set_style_information(styles_Live)

                else:
                        styles_Live = {
                            "Not_Critical_live_view": "background-color:rgb(213, 213, 0)",
                            "Critical_live_view": "background-color:rgb(219, 219, 219) ",
                            "Normal_live_view": "background-color:rgb(219, 219, 219)",
                        }
                        self.ui_live.set_style_information(styles_Live)

            #"background-color:rgb(219, 219, 219); border-radius : 50; border : 2px solid black"
            self.show_image(res_img)
            cv2.waitKey(1)
