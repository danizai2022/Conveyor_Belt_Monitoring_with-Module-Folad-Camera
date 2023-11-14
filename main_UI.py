import sys
from main_API import main_API
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, uic
from PageUI.LiveView_UI import LiveView_UI
from PageUI.Report_UI import Report_UI
from PageUI.CameraSetting_UI import CameraSetting_UI
from PageUI.AlgorithmCalibration_UI import AlgorithmCalibration_UI
from PageUI.Common_Function_UI import Common_Function_UI 

MAIN_UI_PATH = "UIFiles/main_UI.ui"

class mainUI:

    """this class is used to build class for mainwindow to load GUI application

    :param QtWidgets: _description_

    """
    def __init__(self, ui):
        """this function is used to laod ui file and build GUI application"""
        self.ui = ui
        self.Page_LiveView = LiveView_UI(self.ui)
        self.Page_Report = Report_UI(self.ui)
        self.Page_AlgorithmCalibration = AlgorithmCalibration_UI(self.ui)
        self.Page_CameraSetting = CameraSetting_UI(self.ui)
        self.common_func=Common_Function_UI()
        self.activate_()
        self.laod_table_parms()


    def laod_table_parms(self):
        #self.tableWidget.verticalHeader().setStretchLastSection(True)
        header = self.ui.tableWidget.horizontalHeader()
        self.ui.tableWidget.horizontalHeaderVisible = True
        #header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.ui.tableWidget.setColumnWidth(0, 60)  


    def load_page(self):
        btn = self.ui.sender()
        btnName = btn.objectName()

        if btnName == "LiveDetectionBT":
            self.ui.stackedWidget.setCurrentWidget(self.ui.Live_View_Page)

        if btnName == "HelpConnectionBT":
            self.ui.stackedWidget.setCurrentWidget(self.ui.Help_page)

        if btnName == "ReportConnectionBT":
            self.ui.stackedWidget.setCurrentWidget(self.ui.Report_page)

        if btnName == "CameraSettingBT":
            self.ui.stackedWidget.setCurrentWidget(self.ui.Camera_Setting_Page)

    def activate_(self):
        """main butoons connect -- exit , minize , maximize, help --"""
        self.ui.close_btn.clicked.connect(self.close_win)
        self.ui.minimize_btn.clicked.connect(self.minimize)
        self.ui.maximize_btn.clicked.connect(self.maxmize_minimize)
        self.ui.LiveDetectionBT.clicked.connect(self.load_page)
        self.ui.HelpConnectionBT.clicked.connect(self.load_page)
        self.ui.ReportConnectionBT.clicked.connect(self.load_page)
        self.ui.CameraSettingBT.clicked.connect(self.load_page)

    def minimize(self):
        """Minimize winodw"""
        self.ui.showMinimized()

    def close_win(self):
        """
        this function closes the app
        Inputs: None
        Returns: None
        """

        res = self.common_func.show_alert_window(
            title="Exit",
            message="Do you want to exit?",
            need_confirm=True,
            level=1,
        )

        if res:
            self.app_close_flag = True
            self.ui.close()
            sys.exit()

    def maxmize_minimize(self):
        """Maximize or Minimize window"""
        if self.ui.isMaximized():
            self.ui.showNormal()
        else:
            self.ui.showMaximized()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = uic.loadUi(MAIN_UI_PATH)
    win.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))
    main_ui = mainUI(win)
    API = main_API(main_ui)
    win.show()
    app.exec_()
