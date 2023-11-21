import pickle
import cv2
import numpy as np
CAMERA_PICKLE_PATH="backend\Camera\dict.camera"
ALGORITHM_PICKLE_PATH="backend\Calibration\dict.pickle"
from Detection.Defect import (
    defect_detection_find_max,

)
class CameraSetting_API:

    """Description of the code

    :param
    
    """

    def __init__(self, ui,camera):
        self.ui_cam = ui  # ui =self.ui.Page_CameraSetting    =====>  self.ui.Page_CameraSetting=CameraSetting_UI(self.ui)  on main_UI page
        self.button_connector()
        self.pre_laod_camera_parms()
        self.pre_laod_algorithm_parms()
        self.button_connector_camera()

        self.camera=camera

    def button_connector(self):
        self.ui_cam.button_connector(self.save_load_camera_param,self.Save_algorithm_parms,self.calculate_tear_depth)


    def button_connector_camera(self,):
        #pass
        self.ui_cam.button_connector_camera(self.show_frame)    ############## for getting image from camera
        ########self.ui_live.button_connector(self.start_selection)  # for getting image from folder


    def calculate_tear_depth(self):
       perspective = np.cos(60 * 3.14159 / 180)  
       if self.camera !=None:
           #self.camera.build_converter(pixel_type=dorsaPylon.PixelType.GRAY8)         ###################  for getting image from  camera
           # self.camera.Operations.start_grabbing()
            #self.camera.Parms.set_exposureTime(5000)
           # self.camera.Parms.set_gain(517)  #217   #### get the good answer
           parms_camera = self.ui_cam.get_camera_parms_UI()
           Exposure=parms_camera["Exposure"]
           Gain=parms_camera["Gain"]

           self.camera.Parms.set_exposureTime(Exposure)      # Get good answer for second version ----- 5000
           self.camera.Parms.set_gain(Gain)  #217   #### get the good answer         # Get good answer for second version ----- 517
           img = self.camera.getPictures()
           img = img[:, 25:620]
           img = cv2.blur(img, (5, 1))
           h, w = img.shape
           total_sum = 0
           total_count = 0

           for i in range(w-1):
              for j in range (h-1):
                  if  img[j,i]>100:
                      #print(img[i,j])
                      total_count += 1
                      total_sum += j
              if total_count>0:
                    a=int((total_sum / total_count)) /(perspective + 0.01)
                    #print("sum of defect")
                    #print(a)
                      
           #max=defect_detection_find_max(img ,470)
           #print(a)
           self.ui_cam.show_tear_depth(a)



    def show_frame(self):
        pass
        ##pass
        ######### pass 
        ###############print("show frame on camera setting page")
        ##################       if self.camera !=None:
            #self.camera.build_converter(pixel_type=dorsaPylon.PixelType.GRAY8)         ###################  for getting image from  camera
            #self.camera.Operations.start_grabbing()
            #self.camera.Parms.set_exposureTime(5000)
            #self.camera.Parms.set_gain(517)  #217   #### get the good answer
         #############################  img = self.camera.getPictures()
         ##############################  self.show_image(img)
           #cv2.imshow("img",img)
          

    def get_Camera_parms(self):
        parms_camera = self.ui_cam.get_camera_parms_UI()
        return parms_camera
     
    def get_Algorithhm_parms(self):
        parms_algorithm = self.ui_cam.get_algorithm_parms_UI()
        return parms_algorithm
     

    def set_back_event_func_camera(self,fun_camera):
        self.set_camera_paprameter_on_main_API=fun_camera


    def set_back_event_func_algorithm(self, fun_algorithm):
         self.set_algorithm_paprameter_on_main_API= fun_algorithm

    def save_load_camera_param(self):
        parms_camera = self.ui_cam.get_camera_parms_UI()
        pickle_out = open(
            CAMERA_PICKLE_PATH, "wb"
        )  # This is used to store parameters of algorithm in the pickle in python
        pickle.dump(parms_camera, pickle_out)
        pickle_out.close()
        self.ui_cam.set_message_on_label("The Parameters of camera is Succussfully Changed")
        self.set_camera_paprameter_on_main_API(parms_camera)  



    def Save_algorithm_parms(self):
        parms_algorithm = self.ui_cam.get_algorithm_parms_UI()
        pickle_out = open(ALGORITHM_PICKLE_PATH, "wb")
        pickle.dump(parms_algorithm, pickle_out)
        pickle_out.close()

        self.ui_cam.set_message_on_label("The Parameters of algorithm is Succussfully Changed")                              
        self.set_algorithm_paprameter_on_main_API(parms_algorithm)                   
      
    def pre_laod_camera_parms(self):
        pickle_in = open(
           CAMERA_PICKLE_PATH, "rb"
        )  # This is used to store parameters of algorithm in the pickle in python
        parms = pickle.load(pickle_in)
        self.ui_cam.set_camera_parms_UI(parms)

    def pre_laod_algorithm_parms(self):
        pickle_in = open(
            ALGORITHM_PICKLE_PATH, "rb"
        )  # This is used to store parameters of algorithm in the pickle in python
        example_dict = pickle.load(pickle_in)
        self.ui_cam.set_algorithm_parms_UI(example_dict)



    def show_image(self, frame):
        img = frame
        # h, w, ch = img.shape
        h, w = img.shape
        img = cv2.resize(
            img,
            # (w, h),  # this is relative to the camera
            (1500, 1000),  # 
            interpolation=cv2.INTER_AREA,
        )

        try:
            h, w, ch = img.shape

        except:
            h, w = img.shape
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            ch = 1
        bytes_per_line = ch * w
        self.ui_cam.set_Pixmap(img.data, w, h, bytes_per_line)