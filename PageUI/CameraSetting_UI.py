from PyQt5.QtWidgets import *
from .Common_Function_UI import Common_Function_UI
from functools import partial
from PyQt5.QtGui import QImage, QPixmap
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
             "Serial_2": self.ui.serial_number_spinBox_2,
            "Gain_2": self.ui.gain_spinbox_2,
            "Exposure_2": self.ui.expo_spinbox_2,
            "Width_2": self.ui.width_spinbox_2,
            "Height_2": self.ui.height_spinbox_2,
            "offsetX_2": self.ui.offsetx_spinbox_2,
            "offsetY_2": self.ui.offsety_spinbox_2,
        }
        self.parms_camera = {
            "Serial": 0,
            "Gain": 0,
            "Exposure": 0,
            "Width": 0,
            "Height": 0,
            "offsetX": 0,
            "offsetY": 0,
            "Serial_2": 0,
            "Gain_2": 0,
            "Exposure_2": 0,
            "Width_2": 0,
            "Height_2": 0,
            "offsetX_2": 0,
            "offsetY_2": 0,
        }

        self.general_information_algorithm = {
            "GRADIENT_SIZE": self.ui.SpinBox_GRADIENT_SIZE,
            "Critical_Depth": self.ui.SpinBox_Critical_Depth,
            "TEAR_DEPTH": self.ui.SpinBox_TEAR_DEPTH,
            "MAX_ERROR": self.ui.SpinBox_MAX_ERROR,
           
        }
        self.parms_algorithm = {
            "GRADIENT_SIZE": 0,
            "Critical_Depth": 0,
            "TEAR_DEPTH": 0,
            "MAX_ERROR": 0,
           
        }

        self.ui.Stop_connection_Camera_setting.setEnabled(False)

    def button_connector(self, fun_camera,fun_algorithm,fun_Tear):
        self.ui.Save_Camera_Parameters.clicked.connect(fun_camera)
        self.ui.Save_Algorithm_Parameters.clicked.connect(fun_algorithm)
        self.ui.Camera_connection_Camera_setting.clicked.connect(
            partial(self.connect_camera)
        )
        self.ui.Show_Tear_Depth_Button.clicked.connect(
        fun_Tear    
        )
        self.ui.Save_Algorithm_Parameters.clicked.connect(fun_algorithm)

    def show_tear_depth(self,max):
         self.ui.Show_Tear_Depth_Label.setText(str(max))


    def button_connector_camera(self,fun):
        self.ui.Camera_connection_Camera_setting.clicked.connect(fun)


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
            if name == "Serial"  or name == "Serial_2":
                self.general_information_camera[name].setText(str(value))
            else:
                self.general_information_camera[name].setValue(value)



    def get_camera_parms_UI(self):
        for name, value in self.general_information_camera.items():
            if name == "Serial"  or name == "Serial_2":
                self.parms_camera[name] = int(
                    self.general_information_camera[name].text()
                )
            else:
                self.parms_camera[name] = int(
                    self.general_information_camera[name].value()
                )

        return self.parms_camera



    def set_algorithm_parms_UI(self, example_dict):
        for name, value in example_dict.items():
            self.general_information_algorithm[name].setValue(value)
       
        self.parms_algorithm = self. get_algorithm_parms_UI()

    def get_algorithm_parms_UI(self):
        for name, value in self.general_information_algorithm.items():
            self.parms_algorithm[name] = int(self.general_information_algorithm[name].value())

        return self.parms_algorithm

    def set_Pixmap(self, img_data, w, h, bytes_per_line):
        convert_to_Qt_format = QImage(
            img_data,
            w,
            h,
            bytes_per_line,
            QImage.Format_Grayscale8,  # This is used to show the heatmap of the defect in output
        )
        self.ui.Showlive_Setting.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
        #self.ui.Showlive.setPixmap(QPixmap.fromImage(convert_to_Qt_format).transformed(QtGui.QTransform().rotate(90)))    ########## for rotate image
