from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from .Common_Function_UI import Common_Function_UI
from backend.Photo_Viewer.Photo_Viewer_UI import PhotoViewer_UI
from PyQt5.QtWidgets import *

PHOTO_VIEWER_UI_PATH = "UIFiles/photo_viewer.ui"

class Report_UI(Common_Function_UI):

    """Description of the code
    :param
    """

    def __init__(self, ui):
        """Description of the code"""

        self.ui = ui
        self.table_information = {
            "tableWidget": self.ui.tableWidget,
        }

        self.general_information_Report = {
            "Min_Depth": self.ui.lineEdit_Min_Depth,
            "Max_Depth": self.ui.lineEdit_Max_Depth,
            "Min_Length": self.ui.lineEdit_Min_Length,
            "Max_Length": self.ui.lineEdit_Max_Length,
            "critical": self.ui.comboBox,
            "Min_Date": self.ui.lineEdit_Min_Date,
            "Max_Date": self.ui.lineEdit_Max_Date,
        }

        self.Info_Report = {
            "Min_Depth": 0,
            "Max_Depth": 0,
            "Min_Length": 0,
            "Max_Length": 0,
            "critical": 0,
            "Min_Date": 0,
            "Max_Date": 0,
        }

    def PhotoViewer(self, image_path):
        window = PhotoViewer_UI(
            ui_file_path=PHOTO_VIEWER_UI_PATH, image_path=image_path
        )
        window.open_win()

    def button_connector(self, func1, func2):
        self.ui.Report.clicked.connect(func1)
        self.ui.Report_Filter.clicked.connect(func2)

    def start_show_report_clear(self):
        self.ui.tableWidget.setRowCount(0)

    def start_show_report(self, records):
       
        self.ui.tableWidget.setRowCount(len(records))

    def Create_Button(self, txt, i, j, fun):
        pb_Detail = QtWidgets.QPushButton()
        pb_Detail.setText(txt)
        #connect_box = QtWidgets.QVBoxLayout()
        #connect_box.setAlignment(QtCore.Qt.AlignLeft
        #connect_box.addWidget( pb_Detail)
        ##############cellWidget = QWidget()
        #################layoutCB = QHBoxLayout(cellWidget)
        ###############layoutCB.addWidget( pb_Detail)
        ###################layoutCB.setAlignment(QtCore.Qt.AlignLeft)            
        #layoutCB.setContentsMargins(0,0,0,0)
        ###############cellWidget.setLayout(layoutCB)
        self.ui.tableWidget.setCellWidget(i, j,pb_Detail)
        pb_Detail.clicked.connect(fun)

    def set_table_information(self, infoes: dict, ID: int):
       for name, value in infoes.items():
            item_table = QTableWidgetItem(value) # create the item                    
            item_table.setTextAlignment(Qt.AlignCenter) # change the alignment       
            self.table_information["tableWidget"].setItem(
                ID, name, item_table
            )
    def alarm_message_for_delete(self, Select_ID):
        res = self.show_alert_window(
            title="Delete",
            message="Do you want to delete the defect with ID-Number of "
            + str(Select_ID)
            + " ?",
            need_confirm=True,
            level=1,
        )

        return res

    def get_table_info(self):
        row = self.ui.tableWidget.currentRow()
        Select_ID = self.ui.tableWidget.item(row, 0).text()
        return Select_ID

    # def set_Pixmap(self, img_data, w, h, bytes_per_line):
    #    convert_to_Qt_format = QImage(
    #       img_data,
    #       w,
    #       h,
    #        bytes_per_line,
    #        QImage.Format_BGR888,  # This is used to show the heatmap of the defect in output
    #    )
    #    self.ui.Showlive.setPixmap(QPixmap.fromImage(convert_to_Qt_format))   # Change the name of ui.Showlive  depend on the name of the lable of current page

    # def show_text(self, text):
    #    self.ui.ID_of_Defect.setText(text)

    def show_text_message(self, text):
        self.set_message(
            label_name=self.ui.Message_Report,
            text=text,
        )

    def get_Report_parms_UI(self):
        for name, value in self.general_information_Report.items():
            if name == "critical":
                self.Info_Report[name] = self.general_information_Report[
                    name
                ].currentText()
            else:
                self.Info_Report[name] = self.general_information_Report[name].text()

        return self.Info_Report

    def get_Report_checkBox_isChecked(self):
        return (
            self.ui.checkBox_Depth.isChecked(),
            self.ui.checkBox_Type.isChecked(),
            self.ui.checkBox_Length.isChecked(),
            self.ui.checkBox_Date.isChecked(),
        )
