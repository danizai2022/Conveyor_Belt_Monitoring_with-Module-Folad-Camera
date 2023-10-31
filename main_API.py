from PageAPI.CameraSetting_API import CameraSetting_API
from PageAPI.AlgorithmCalibration_API import AlgorithmCalibration_API
from PageAPI.LiveView_API import LiveView_API
from PageAPI.Report_API import Report_API
from Database.mainDatabase import mainDatabase

class main_API:

    """Description of the code

    """
    def __init__(self, ui) -> None:

        self.ui = ui  #    ========================= > API = main_API(main_ui)  on main_UI page
        self.db = mainDatabase()
        ###############################      AlgorithmCalibration_API    ################################
        self.API_Page_AlgorithmCalibration = AlgorithmCalibration_API(
            self.ui.Page_AlgorithmCalibration
        )  # Create Object of AlgorithmCalibration_API  =========== > self.Page_AlgorithmCalibration = AlgorithmCalibration_UI(self.ui)  on main_UI page
        self.API_Page_AlgorithmCalibration.set_back_event_func(self.get_calibration_paprameter_main_API)
        param_calibration_API=self.API_Page_AlgorithmCalibration.get_Calibration_parms()
      
        ###############################      CameraSetting_API    ################################
        self.API_Page_CameraSetting = CameraSetting_API(
            self.ui.Page_CameraSetting
        )# Create Object of CameraSetting_API   =========== >self.ui.Page_CameraSetting=CameraSetting_UI(self.ui)  on main_UI page
        self.API_Page_CameraSetting.set_back_event_func(self.get_camera_paprameter_main_API)
        param_camera_API=self.API_Page_CameraSetting.get_Camera_parms()
        

        ###############################      LiveView_API    ################################
        self.API_Page_LiveView = LiveView_API(
            self.ui.Page_LiveView,self.db.Report_DB 
        )  # Create Object of Page_LiveView   =========== > self.Page_LiveView = LiveView_UI(self.ui)  on main_UI page
        self.API_Page_LiveView.set_initial_param_calibration(param_calibration_API)
        self.API_Page_LiveView.set_initial_param_camera(param_camera_API)


        ###############################      Report_API    ################################
        self.API_Page_Report = Report_API(
            self.ui.Page_Report,self.db.Report_DB
        )  # Create Object of Report_API   =========== >self.Page_Report = Report_UI(self.ui)  on main_UI page
       

    def get_calibration_paprameter_main_API(self,param):
         self.API_Page_LiveView.set_param_calibration(param)
        

    def get_camera_paprameter_main_API(self,param):
         self.API_Page_LiveView.set_param_camera(param)

        