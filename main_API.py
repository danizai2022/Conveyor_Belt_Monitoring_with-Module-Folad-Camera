from PageAPI.CameraSetting_API import CameraSetting_API
from PageAPI.AlgorithmCalibration_API import AlgorithmCalibration_API
from PageAPI.LiveView_API import LiveView_API
from PageAPI.Report_API import Report_API
from Database.mainDatabase import mainDatabase
from backend.Camera.dorsaPylon import Collector, Camera
class main_API:

    """
    Description of the code

    """
    def __init__(self, ui) -> None:



        
        self.collector = Collector()
                 
        ###################  self.camera = self.collector.get_camera_by_serial(str(self.parms_camera_liveView["Serial"]))
        self.camera = self.collector.get_camera_by_serial(str(23287291))    ###################  for getting image from  camera
       
       
        self.ui = ui  #============================== > API = main_API(main_ui)  on main_UI page
        self.db = mainDatabase()
        ###############################      AlgorithmCalibration_API    ################################
        self.API_Page_AlgorithmCalibration = AlgorithmCalibration_API(
            self.ui.Page_AlgorithmCalibration
        )  # Create Object of AlgorithmCalibration_API  =========== > self.Page_AlgorithmCalibration = AlgorithmCalibration_UI(self.ui)  on main_UI page
        self.API_Page_AlgorithmCalibration.set_back_event_func(self.get_calibration_paprameter_main_API)   #  introduce and send the name of the  "get_calibration_paprameter_main_API" function to AlgorithmCalibration_API to call this function when the parameters of the calibration is changed on "Save_Calibration_parms"  function in AlgorithmCalibration_API
        param_calibration_API=self.API_Page_AlgorithmCalibration.get_Calibration_parms()     # for getting the initial parameters of the Calibration
        
        ###############################      CameraSetting_API    ################################
        self.API_Page_CameraSetting = CameraSetting_API(
            self.ui.Page_CameraSetting,self.camera
        )# Create Object of CameraSetting_API   =========== >self.ui.Page_CameraSetting=CameraSetting_UI(self.ui)  on main_UI page
        self.API_Page_CameraSetting.set_back_event_func_camera(self.get_camera_paprameter_main_API)   # introduce and send the name of the  "get_camera_paprameter_main_API"  function to API_Page_CameraSetting to call this function when the parameters of the camera is changed
        self.API_Page_CameraSetting.set_back_event_func_algorithm(self.get_algorithm_paprameter_main_API)   # introduce and send the name of the  "get_camera_paprameter_main_API"  function to API_Page_CameraSetting to call this function when the parameters of the camera is changed
        param_camera_API=self.API_Page_CameraSetting.get_Camera_parms()        # for getting the initial parameters of the Camera_Setting
        param_Alghorithm_API=self.API_Page_CameraSetting.get_Algorithhm_parms()        # for getting the initial parameters of the Camera_Setting

        ###############################      LiveView_API    ################################
        self.API_Page_LiveView = LiveView_API(
            self.ui.Page_LiveView,self.db.Report_DB ,self.camera
        )  # Create Object of Page_LiveView   =========== > self.Page_LiveView = LiveView_UI(self.ui)  on main_UI page
        self.API_Page_LiveView.set_initial_param_calibration(param_calibration_API)  # set the initial param of the calibration on liveViewPage
        self.API_Page_LiveView.set_initial_param_camera(param_camera_API)            # set the initial param  of the camera on liveViewPage
        self.API_Page_LiveView.set_initial_param_algorithm(param_Alghorithm_API) 

        ################################      Report_API    ################################
        self.API_Page_Report = Report_API(
            self.ui.Page_Report,self.db.Report_DB
        )  # Create Object of Report_API   =========== >self.Page_Report = Report_UI(self.ui)  on main_UI page


    def get_calibration_paprameter_main_API(self,param):
         self.API_Page_LiveView.set_param_calibration(param)  # Send the parameters of calibration to API_Page_liveView
        

    def get_camera_paprameter_main_API(self,param):
         self.API_Page_LiveView.set_param_camera(param)   # Send the parameters of camera to API_Page_liveView

    
    def get_algorithm_paprameter_main_API(self,param):
         self.API_Page_LiveView.set_param_algorithm(param)   # Send the parameters of camera to API_Page_liveView
        
        

    