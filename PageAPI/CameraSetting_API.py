import pickle
CAMERA_PICKLE_PATH="backend\Camera\dict.camera"
ALGORITHM_PICKLE_PATH="backend\Calibration\dict.pickle"
class CameraSetting_API:

    """Description of the code

    :param
    
    """

    def __init__(self, ui,camera):
        self.ui_cam = ui  # ui =self.ui.Page_CameraSetting    =====>  self.ui.Page_CameraSetting=CameraSetting_UI(self.ui)  on main_UI page
        self.button_connector()
        self.pre_laod_camera_parms()
        self.pre_laod_algorithm_parms()
        self.camera=camera

    def button_connector(self):
        self.ui_cam.button_connector(self.save_load_camera_param,self.Save_algorithm_parms)


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

