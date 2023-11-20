from Database.databaseManager import databaseManager
import cv2

class Report_API:

    """Description of the code

    :param
    """

    def __init__(self, ui,db):
        self.ui_re = ui
        self.step = 2
        self.pix_mm_depth = 0.34
        self.pix_mm_width = 140 / 590
        self.CONVAYER_SPEED = 120  # mm/s
        self.pix_mm_length = self.step * self.CONVAYER_SPEED / 400    ########### 750    
        self.db_report=db
        #self.db_report = databaseManager(
        #    "root", "dorsa-co", "localhost", "test_database"
        #)
        self.button_connector()

    def button_connector(self):
        self.ui_re.button_connector(self.Show_Report, self.Show_Report_Filter)


    def Show_Report(self):
        """
        This function is used to show the result in the QTableWidget
        """

        records = self.db_report.get_all_content()
        self.ui_re.start_show_report_clear()
        self.ui_re.start_show_report(records)

        for i in range(0, len(records)):
            if records[i]["critical"] == 0:
                str_critical = "Not Critical Defect"

            if records[i]["critical"] == 1:
                str_critical = "Critical Defect"
            infoes = {
                0: "{:.0f}".format(int(records[i]["id"])),
                1: "{:.2f}".format(float(records[i]["Length"])) + " " + "mm",
                2: "{:.2f}".format(float(records[i]["Depth"])) + " " + "mm",
                3: "{:.2f}".format(float(records[i]["width"])) + " " + "mm",
                4: str(records[i]["Date"]),
                5: str_critical,
            }
            self.ui_re.set_table_information(infoes, i)
            self.ui_re.Create_Button("Show Defect", i, 6, self.pb_Detail_Function)
            self.ui_re.Create_Button("Delete Defect", i, 7, self.pb_Delete_Function)

    def pb_Delete_Function(self):
        
        Select_ID = self.ui_re.get_table_info()
        res = self.ui_re.alarm_message_for_delete(Select_ID)
        if res:
            records = self.db_report.remove_record("id", Select_ID)
            if records:
                self.ui_re.show_text_message(
                    text="Successfully remove the defect with ID-Number of "
                    + str(Select_ID)
                )
            else:
                self.ui_re.show_text_message(
                    text="Unsuccessfully remove the defect with-ID Number of "
                    + str(Select_ID)
                )
            self.Show_Report()

    def pb_Detail_Function(self):
        Select_ID = self.ui_re.get_table_info()
        records = self.db_report.search("id", Select_ID)
        image_path = records[0]["image_path"]
        # img_roi = cv2.imread(image_path)
        self.ui_re.PhotoViewer(image_path)
        # self.ui_re.show_text(" " + str(records[0]["id"]) + " ")
        # self.show_image(img_roi)

    def Show_Report_Filter(self):
        """
        This function is used to show the result in the QTableWidget
        """
        self.ui_re.start_show_report_clear()
        flage = [1, 1, 1, 1]
        inter = []
        intersect = []

        param_report = self.ui_re.get_Report_parms_UI()
      
        (
            checkBox_Depth,
            checkBox_Type,
            checkBox_Length,
            checkBox_Date,
        ) = self.ui_re.get_Report_checkBox_isChecked()

        if (
            not checkBox_Depth
            and not checkBox_Type
            and not checkBox_Length
            and not checkBox_Date
        ):
            self.ui_re.show_text_message(text="Please Select one Filter ")

        else:
            if checkBox_Length:
                records_Length = self.db_report.search_interval(
                    "Length",
                    param_report["Min_Length"],
                    param_report["Max_Length"],
                )
                inter.append(records_Length)
                flage[0] = 1
            else:
                records_Length = []
                inter.append(records_Length)
                flage[0] = 0

            if checkBox_Depth:
                records_Depth = self.db_report.search_interval(
                    "Depth",
                    param_report["Min_Depth"],
                    param_report["Max_Depth"],
                )

                inter.append(records_Depth)
                flage[1] = 1
            else:
                records_Depth = []
                inter.append(records_Depth)
                flage[1] = 0
            if checkBox_Type:
                if param_report["critical"] == "Critical":
                    records_Type = self.db_report.search("critical", 1)
                    inter.append(records_Type)
                    flage[2] = 1

                else:
                    records_Type = self.db_report.search("critical", 0)
                    inter.append(records_Type)
                    flage[2] = 1
            else:
                records_Type = []
                inter.append(records_Type)
                flage[2] = 0

            if checkBox_Date:
                records_Date = self.db_report.search_interval(
                    "Date",
                    param_report["Min_Date"],
                    param_report["Max_Date"],
                )
                inter.append(records_Date)
                flage[3] = 1
            else:
                records_Date = []
                inter.append(records_Date)
                flage[3] = 0

            for i in range(len(flage)):
                if flage[i] == 1:
                    intersect.append(inter[i])

            records = intersect[0]
            for i in range(1, len(intersect)):
                dd = intersect[i]
                records = [x for x in records if x in dd]

            self.ui_re.start_show_report(records)

            for i in range(0, len(records)):
                if records[i]["critical"] == 0:
                    str_critical = "Not Critical Defect"

                if records[i]["critical"] == 1:
                    str_critical = "Critical Defect"
                infoes = {
                    0: "{:.0f}".format(int(records[i]["id"])),
                    1: "{:.2f}".format(float(records[i]["Length"])) + " " + "mm",
                    2: "{:.2f}".format(float(records[i]["Depth"])) + " " + "mm",
                    3: "{:.2f}".format(float(records[i]["width"])) + " " + "mm",
                    4: str(records[i]["Date"]),
                    5: str_critical,
                }
                self.ui_re.set_table_information(infoes, i)
                self.ui_re.Create_Button("Show Defect", i, 6, self.pb_Detail_Function)
                self.ui_re.Create_Button("Delete Defect", i, 7, self.pb_Delete_Function)

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
        self.ui_re.set_Pixmap(img.data, w, h, bytes_per_line)
