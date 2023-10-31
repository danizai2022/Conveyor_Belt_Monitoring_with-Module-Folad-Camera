import pickle
CAMERA_PICKLE_PATH="backend\Camera\dict.camera"
class CameraSetting_API:

    """Description of the code

    :param
    
    """

    def __init__(self, ui):
        self.ui_cam = ui  # ui =self.ui.Page_CameraSetting    =====>  self.ui.Page_CameraSetting=CameraSetting_UI(self.ui)  on main_UI page
        self.button_connector()
        self.pre_laod_camera_parms()


    def button_connector(self):
        self.ui_cam.button_connector(self.save_load_camera_param)


    def get_Camera_parms(self):
        parms = self.ui_cam.get_camera_parms_UI()
        return parms
     

    def set_back_event_func(self,fun):
        self.set_camera_paprameter_on_main_API=fun


    def save_load_camera_param(self):
        parms = self.ui_cam.get_camera_parms_UI()
        pickle_out = open(
            CAMERA_PICKLE_PATH, "wb"
        )  # This is used to store parameters of algorithm in the pickle in python
        pickle.dump(parms, pickle_out)
        pickle_out.close()
        self.ui_cam.set_message_on_label("The Parameters is Succussfully Changed")
        self.set_camera_paprameter_on_main_API(parms)  


    def pre_laod_camera_parms(self):
        pickle_in = open(
           CAMERA_PICKLE_PATH, "rb"
        )  # This is used to store parameters of algorithm in the pickle in python
        parms = pickle.load(pickle_in)
        self.ui_cam.set_camera_parms_UI(parms)


