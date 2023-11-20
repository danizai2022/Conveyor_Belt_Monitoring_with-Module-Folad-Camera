import cv2
import numpy as np
# from utils.Defect2 import getDate
from datetime import date
import jdatetime


PATH_of_SAVE_IMAGE="Detection/image6/imagess_"

class defectTracker:
    def __init__(self, min_g_thresh, step_per_line, db_Report) -> None:
        self.min_g_thresh = min_g_thresh
        self.step_per_line = step_per_line

        self.complete_defects_cnts = (
            []
        )  # This list is used to store the complete_defect_cnt
        self.inprogress_defects_cnts2 = (
            []
        )  # This list is used to store the inprogress_defect_cnt
        self.inprogress_defects_cnts = (
            []
        )  # This list is used to store the inprogress_defect_cnt

        ###############   add by myself  ############
        self.total_complete_defects_cnts = []
        self.total_depth = []
        self.critical_flage = []
        self.number_of_defect = 0
        self.number_of_critical_defect = 0
        self.total_area_of_defect = 0
        self.step = 2
        #######self.pix_mm_depth = 0.4
        self.pix_mm_depth = 0.34
        # self.pix_mm_width = 140 / 640
        self.pix_mm_width = 140 / 590
        self.CONVAYER_SPEED = 120  # mm/s
        ######self.pix_mm_length = self.step * self.CONVAYER_SPEED / 1000
        self.pix_mm_length = self.step * self.CONVAYER_SPEED / 400   ############## 750
        self.db_Report = db_Report
        self.max_depth=0

    def refresh(self, img, depth_img, pix_length, pix_width,Critical_Depth1,Critical_Width,Critical_Lenght,not_Critical_Depth1,not_Critical_Width,not_Critical_Lenght,not_Critical_Depth1_Max,not_Critical_Width_Max,not_Critical_Lenght_Max):
        self.pix_mm_width= pix_width
        self.pix_mm_length=pix_length
        h_img, w_img = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
        thresh_img = cv2.erode(thresh_img, np.ones((3, 3)), iterations=1)
        thresh_img = cv2.dilate(thresh_img, np.ones((3, 3)), iterations=4)
        thresh_img = cv2.erode(thresh_img, np.ones((3, 3)), iterations=3)

        not_remove_cnts = []
        for cnt in self.complete_defects_cnts:
            cnt[:, 0, 1] -= self.step_per_line
            if np.max(cnt[:, 0, 1]) <= 0:
                pass
            else:
                not_remove_cnts.append(cnt)

        self.complete_defects_cnts = not_remove_cnts

        cv2.drawContours(
            thresh_img, self.complete_defects_cnts, -1, color=0, thickness=-1
        )
        contours, _ = cv2.findContours(
            thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        self.inprogress_defects_cnts = []
        self.max_depth=0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 300:  # or perimeter > 100:   # filter the area of the defect
                critical_flage_id = 2
                ######### I changed this part
                ####if area > 300:  # or perimeter > 100:   # filter the area of the defect
                # print("area of defect")
                # print(area)
                x, y, w, h = cv2.boundingRect(cnt)

                if (
                    y + h < h_img - self.min_g_thresh
                ):  # if the defect is completed, then we add it to complete_defects_cnts list
                    # {"bbox": (x, y, w, h), "cnt": cnt}

                    self.complete_defects_cnts.append(cnt)
                    self.total_complete_defects_cnts.append(cnt)

                    self.total_area_of_defect = (
                        cv2.contourArea(cnt) * self.pix_mm_length * self.pix_mm_width
                    ) + self.total_area_of_defect
                    w_mm = w * self.pix_mm_width
                    h_mm = h * self.pix_mm_length
                    defect_roi = depth_img[max(y, 0) : y + h, x : x + w]
                    roi = img[y : y + h, x : x + w]
                    # cv2.imshow("img", roi)

                    self.total_depth.append(
                        abs(defect_roi).max()
                    )  # Find the depth of the defect

                    if abs(defect_roi).max() > Critical_Depth1  and w_mm > Critical_Width   and h_mm > Critical_Lenght :


                        self.number_of_critical_defect = (
                            self.number_of_critical_defect + 1
                        )
                        critical_flage_id = 1
                        self.critical_flage.append(
                            1
                        )  # If defect is critical, the flage is set to 1
                    #else:
                         #print("abs(defect_roi).max()")
                         #print(abs(defect_roi).max())
                         #print("w_mm")
                         #print(w_mm)
                         #print("h_mm")
                         #print(h_mm)

                         #print(not_Critical_Depth1)
                         #print(not_Critical_Width)
                         #print(not_Critical_Lenght)

                        # print("abs(defect_roi).max()  >  not_Critical_Depth1")
                        # print(abs(defect_roi).max()  >  not_Critical_Depth1)
                       #  print( abs(defect_roi).max() < Critical_Depth1 )
                        # print(w_mm > not_Critical_Width)
                        # print( w_mm < Critical_Width)
                        # print(h_mm > not_Critical_Lenght)
                        # print( h_mm < Critical_Lenght)


                   
                    else :
                        if abs(defect_roi).max()  >  not_Critical_Depth1  and   abs(defect_roi).max() < not_Critical_Depth1_Max :
                         if  w_mm > not_Critical_Width  and  w_mm < not_Critical_Width_Max :
                               if  h_mm > not_Critical_Lenght  and  h_mm < not_Critical_Lenght_Max:         
                         # if abs(defect_roi).max()  >  not_Critical_Depth1  and  w_mm > not_Critical_Width   and  h_mm > not_Critical_Lenght:
                                    critical_flage_id = 0
                                    self.critical_flage.append(
                                                    0
                                    )  # If defect is not-critical, the flage is set to 0
                        else :    
                            critical_flage_id = 2  
                            self.number_of_defect = self.number_of_defect + 1  
                    # if len (self.total_complete_defects_cnts)> 0:
                    # print("self.complete_defects_cnts")
                    # print(len(self.total_complete_defects_cnts))
                    if critical_flage_id == 0 or critical_flage_id == 1 :
                       # print("self.number_of_defect")
                        #print(self.number_of_defect )
                       
                        ###str_date = self.getDate_of_system()
                        #str_date = date.today().strftime('%Y/%m/%d')    # This is used for getting the date and time in normal format
                        str_date = date.today().strftime('%Y/%#m/%#d')   # This is used for getting the date and time in decimal format
                        self.max_depth=abs(defect_roi).max()
                        records=self.db_Report.search_Total()
                        if len(records) < 20 :
                            path = PATH_of_SAVE_IMAGE + str(self.number_of_defect) + ".jpg"
                            cv2.imwrite(
                                PATH_of_SAVE_IMAGE + str(self.number_of_defect) + ".jpg",
                                roi,
                            )
                            self.db_Report.add_record(
                                (
                                    h_mm,
                                    abs(defect_roi).max(),
                                    w_mm,
                                    str_date,
                                    critical_flage_id,
                                    path,
                                ),
                            )
                        self.number_of_defect = self.number_of_defect + 1
                else:
                    self.inprogress_defects_cnts.append(cnt)
                   

            else:  # or perimeter > 100:
                self.inprogress_defects_cnts2.append(cnt)
               
        return self.max_depth
        

    def get_defect_infoes(self, depth_img, img):
        h_img, w_img = img.shape[:2]
        all_cnts = self.inprogress_defects_cnts + self.complete_defects_cnts
        for cnt in all_cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            if y + h < h_img - self.min_g_thresh:
                # if y + h < h_img - 30:
                # print(self.min_g_thresh)
                w_mm = w * self.pix_mm_width
                h_mm = h * self.pix_mm_length
                defect_roi = depth_img[max(y, 0) : y + h, x : x + w]
                mean_depth_mm = defect_roi[abs(defect_roi) > 0].mean()
                # print(abs(defect_roi).max())
                return abs(defect_roi).max()

    #  return res

    def draw(self, img, color=(0, 0, 255), thickness=2):
        res = img.copy()
        res = cv2.blur(res, (3, 3))
        all_cnts = self.inprogress_defects_cnts + self.complete_defects_cnts
        #all_cnts2 = self.inprogress_defects_cnts2

        for cnt in all_cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            # rand_color = np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)
            cv2.rectangle(res, (x, y), (x + w, y + h), color=color, thickness=thickness)
            defect_roi = img[y : y + h, x : x + w]
            mean_intensity = defect_roi[defect_roi > 0].mean()


       ## for cnt in all_cnts2:
       ##      x, y, w, h = cv2.boundingRect(cnt)
            # Rand_color = np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)
       ##     cv2.rectangle(res, (x, y), (x + w, y + h), color=(0, 0, 0), thickness=-1)

        return res

    def function_return_complete_defects_cnts(self):
        return self.complete_defects_cnts

    def function_return_critical_flage(self):
        return self.critical_flage

    def function_return_total_depth(self):
        return self.total_depth

    def function_inprogress_defects_cnts(self):
        return self.inprogress_defects_cnts

    def function_number_of_defect(self):
        return self.number_of_defect

    def function_number_of_critical_defect(self):
        return self.number_of_critical_defect

    def function_total_area_of_defect(self):
        return self.total_area_of_defect

    def function_total_complete_defects_cnts(self):
        return self.total_complete_defects_cnts

    def function_inprogress_defects_cnts_x_y_w_h(self, depth_img, img):
        # res = img2.copy()
        # res = cv2.blur(res, (5, 5))
        h_img, w_img = img.shape[:2]
        all_cnts = self.inprogress_defects_cnts + self.complete_defects_cnts
        # all_cnts2 = self.inprogress_defects_cnts

        depth_pr = 0
        for cnt in all_cnts:
            x, y, w, h = cv2.boundingRect(cnt)

            if y + h < h_img - self.min_g_thresh:
                depth_pr = self.total_depth[self.function_number_of_defect() - 1]

            else:
                defect_roi = depth_img[
                    max(y, 0) : y + h, x : x + w
                ]  # find the location of the defect
                depth_pr = abs(defect_roi).max()

            return x, y, w, h, depth_pr

    def getDate_of_system(self):
        this_year = date.today().year
        this_month = date.today().month
        this_day = date.today().day
        str_date = jdatetime.date.fromgregorian(
            day=this_day, month=this_month, year=this_year
        )
        return str_date
