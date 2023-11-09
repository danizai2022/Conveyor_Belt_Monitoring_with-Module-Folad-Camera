import pickle

CALIBRATION_PICKLE_PATH = "backend\Calibration\dict.pickle"


class AlgorithmCalibration_API:

    """Description of the code

    :param
    """

    def __init__(self, ui):
        self.ui_cal = ui
        self.button_connector()
        self.laod_calibration_parms()

    def button_connector(self):
        self.ui_cal.button_connector(self.Save_Calibration_parms)

    def get_Calibration_parms(self):
        example_dict = self.ui_cal.get_calibration_parms_UI()
        return example_dict

    def Save_Calibration_parms(self):
        example_dict = self.ui_cal.get_calibration_parms_UI()

        pickle_out = open(CALIBRATION_PICKLE_PATH, "wb")
        pickle.dump(example_dict, pickle_out)
        pickle_out.close()

        self.ui_cal.set_message_on_label("The Parameters is Succussfully Changed")
        Param_of_Calibration=self.get_Calibration_parms()
        self.set_calibration_paprameter_on_main_API(Param_of_Calibration)
      
    def set_back_event_func(self,fun):
        self.set_calibration_paprameter_on_main_API=fun

    def laod_calibration_parms(self):
        pickle_in = open(
            CALIBRATION_PICKLE_PATH, "rb"
        )  # This is used to store parameters of algorithm in the pickle in python
        example_dict = pickle.load(pickle_in)
        self.ui_cal.set_calibration_parms_UI(example_dict)
