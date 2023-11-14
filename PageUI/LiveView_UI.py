from PyQt5.QtWidgets import *
from functools import partial
from .Common_Function_UI import Common_Function_UI
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


class LiveView_UI(Common_Function_UI):

    """Description of the code

    :param
    """

    def __init__(self, ui):
        """Description of the code"""

        self.ui = ui
        self.general_information_live = {
            "Length": self.ui.Length,
            "Width": self.ui.Width,
            "Depth": self.ui.Depth,
            "Total_Number_Defect": self.ui.Total_Number_Defect,
            "Total_Number_Critical_defect": self.ui.Total_Number_Critical_defect,
        }
        self.style_information_live = {
            "Not_Critical_live_view": self.ui.Not_Critical_live_view,
            "Critical_live_view": self.ui.Critical_live_view,
            "Normal_live_view": self.ui.Normal_live_view,
        }

        self.ui.Stop_connection.setEnabled(False)
        self.ui.live.setEnabled(False)
        self.ui.Stop.setEnabled(False)
        self.camera_connection=False
    def button_connector(self,camera_connection):   # input fun for getting image from folder
        self.camera_connection=camera_connection
        self.ui.Camera_connection.clicked.connect(partial(self.connect_camera))
        self.ui.Stop_connection.clicked.connect(partial(self.disconnect_camera))
       

       # self.ui.live.clicked.connect(
       #     fun
       # )  ###################  for getting image from  folder

    def Set_fn(self, fun):
        self.fn = fun

    def Get_fn(self):
        return self.fn

    def button_connector_QTimer(self, fun):
        self.Set_fn(fun)
        self.ui.live.clicked.connect(self.button_connector_QTimer_fun)

    def button_connector_stop(self):
        
       self.ui.Stop.clicked.connect(self.stop_live)
      

    def stop_live(self):
        self.picktimer.stop()
        self.ui.live.setEnabled(True)
        self.ui.Stop.setEnabled(False)

    def button_connector_QTimer_fun(self):
        fun = self.Get_fn()
        self.picktimer = QTimer()
        self.picktimer.timeout.connect(fun)
        self.picktimer.start()

    def connect_camera(self):
        ##print("connect_camera")
        ##self.enable_disable_camera_btns(True)
        if self.camera_connection !=None:
           
            self.ui.Camera_connection.setEnabled(False)
            #self.camera_connection.Operations.start_grabbing()
            self.set_message(
                label_name=self.ui.Message_LiveView,
                text="Connect to Camera Successfully",
            )

            self.ui.Stop_connection.setEnabled(True)
            self.ui.live.setEnabled(True)

        else :
            self.set_message(
            label_name=self.ui.Message_LiveView,
            text="Please check the connection to the camera",
        )
    def disable_live(self):
        self.ui.live.setEnabled(False)

    def enable_stop(self):
        self.ui.Stop.setEnabled(True)


    def disconnect_camera(self):  
        
        #print("disconnect_camera")
        #self.enable_disable_camera_btns(False)
        #print("self.camera_connection.Operations.stop_grabbing()")
        #print(self.camera_connection.Operations.stop_grabbing())
       
        self.camera_connection.Operations.stop_grabbing()   ################################## Check whether is it work correct or not
        #self.ui.Camera_connection.setEnabled(True)
        self.set_message(
            label_name=self.ui.Message_LiveView,
            text="Disconnect to Camera Successfully",
        )
        self.ui.live.setEnabled(False)
        self.ui.Stop_connection.setEnabled(False)
        self.ui.Camera_connection.setEnabled(True)

    def set_general_information(self, infoes: dict):
        for name, value in infoes.items():
            self.general_information_live[name].setText(value)

    def set_style_information(self, styles: dict):
        for name, value in styles.items():
            self.style_information_live[name].setStyleSheet(value)

    def set_Pixmap(self, img_data, w, h, bytes_per_line):
        convert_to_Qt_format = QImage(
            img_data,
            w,
            h,
            bytes_per_line,
            QImage.Format_BGR888,  # This is used to show the heatmap of the defect in output
        )
        self.ui.Showlive.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
