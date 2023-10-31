from PyQt5.QtWidgets import *
from .Common_Function_UI import Common_Function_UI
from functools import partial



class CameraSetting_UI(Common_Function_UI):

    """Description of the code"""

    def __init__(self, ui):
        self.ui = ui  # self.Page_CameraSetting = CameraSetting_UI(self.ui)   on main_UI
        self.general_information_camera = {
            "Serial": self.ui.serial_number_spinBox,
            "Gain": self.ui.gain_spinbox,
            "Exposure": self.ui.expo_spinbox,
            "Width": self.ui.width_spinbox,
            "Height": self.ui.height_spinbox,
            "offsetX": self.ui.offsetx_spinbox,
            "offsetY": self.ui.offsety_spinbox,
        }
        self.parms_camera = {
            "Serial": 0,
            "Gain": 0,
            "Exposure": 0,
            "Width": 0,
            "Height": 0,
            "offsetX": 0,
            "offsetY": 0,
        }
        self.ui.Stop_connection_Camera_setting.setEnabled(False)

    def button_connector(self, fun):
        self.ui.Save_Camera_Parameters.clicked.connect(fun)
        self.ui.Camera_connection_Camera_setting.clicked.connect(
            partial(self.connect_camera)
        )
        self.ui.Stop_connection_Camera_setting.clicked.connect(
            partial(self.disconnect_camera)
        )

    def connect_camera(self):
        self.ui.Camera_connection_Camera_setting.setEnabled(False)
        self.set_message(
            label_name=self.ui.Message_Camera,
            text="Connect to Camera Successfully",
        )

        self.ui.Stop_connection_Camera_setting.setEnabled(True)

    def disconnect_camera(self):
        # print("disconnect_camera")
        # self.enable_disable_camera_btns(False)
        self.ui.Camera_connection_Camera_setting.setEnabled(True)
        self.ui.Stop_connection_Camera_setting.setEnabled(False)
        self.set_message(
            label_name=self.ui.Message_Camera,
            text="Disconnect to Camera Successfully",
        )

    def set_message_on_label(self, txt):
        self.set_message(
            label_name=self.ui.Message_Camera,
            text=txt,
        )

    def set_camera_parms_UI(self, infoes: dict):
        for name, value in infoes.items():
            if name == "Serial":
                self.general_information_camera[name].setText(str(value))
            else:
                self.general_information_camera[name].setValue(value)



    def get_camera_parms_UI(self):
        for name, value in self.general_information_camera.items():
            if name == "Serial":
                self.parms_camera[name] = int(
                    self.general_information_camera[name].text()
                )
            else:
                self.parms_camera[name] = int(
                    self.general_information_camera[name].value()
                )

        return self.parms_camera
