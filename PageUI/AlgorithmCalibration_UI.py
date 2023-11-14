from PyQt5.QtWidgets import *
from .Common_Function_UI import Common_Function_UI
from functools import partial


class AlgorithmCalibration_UI(Common_Function_UI):

    """Description of the code"""

    def __init__(self, ui):
        """Description of the code"""
        self.ui = ui

        self.general_information_calib = {
            "Width_critical": self.ui.Width_critical,
            "Depth_Critical": self.ui.Depth_Critical,
            "Lenght_Critical": self.ui.Lenght_Critical,
             "Width_not_critical": self.ui.Width_not_critical,
            "Depth_not_Critical":self.ui.Depth_not_Critical,
            "lenght_not_critical": self.ui.lenght_not_critical,
            "Width_not_critical_Max": self.ui.Width_not_critical_Max,
            "Depth_not_Critical_Max":self.ui.Depth_not_Critical_Max,
            "lenght_not_critical_Max": self.ui.lenght_not_critical_Max,
        }
        self.parms_calib = {
            "Width_critical": 0,
            "Depth_Critical": 0,
            "Lenght_Critical": 0,
             "Width_not_critical": 0,
            "Depth_not_Critical":0,
            "lenght_not_critical": 0,
            "Width_not_critical_Max": 0,
            "Depth_not_Critical_Max":0,
            "lenght_not_critical_Max": 0,
        
        }

    def button_connector(self, fun):
        self.ui.Save_Calibration.clicked.connect(fun)
        self.ui.Camera_connection_Calibration.clicked.connect(
            partial(self.connect_camera)
        )
        self.ui.Stop_connection_Clibration.clicked.connect(
            partial(self.disconnect_camera)
        )

    def set_message_on_label(self, txt):
        self.set_message(
            label_name=self.ui.Message_Calibration,
            text=txt,
        )

    def connect_camera(self):
        ##self.enable_disable_camera_btns(True)
        self.ui.Camera_connection_Calibration.setEnabled(False)
        self.set_message(
            label_name=self.ui.Message_Calibration,
            text="Connect to Camera Successfully",
        )

        self.ui.Stop_connection_Clibration.setEnabled(True)

    def disconnect_camera(self):
        # self.enable_disable_camera_btns(False)
        self.ui.Camera_connection_Calibration.setEnabled(True)
        self.ui.Stop_connection_Clibration.setEnabled(False)
        self.set_message(
            label_name=self.ui.Message_Calibration,
            text="Disconnect to Camera Successfully",
        )

    def set_calibration_parms_UI(self, example_dict):
        for name, value in example_dict.items():
            self.general_information_calib[name].setValue(value)
       
        self.parms_calib = self.get_calibration_parms_UI()

    def get_calibration_parms_UI(self):
        for name, value in self.general_information_calib.items():
            self.parms_calib[name] = int(self.general_information_calib[name].value())

        return self.parms_calib
