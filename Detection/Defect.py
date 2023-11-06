import cv2
import numpy as np
from . import heatMap
from . import ConvayerBase
import os

from datetime import date
import jdatetime
from scipy.optimize import curve_fit


GRADIANT_SIZE = 100 # 100
MAX_ERROR =10
# gradiant = heatMap.G11.generate_gradiant(GRADIANT_SIZE)   #Previous version
######gradiant = heatMap.G12.generate_gradiant(GRADIANT_SIZE)
gradiant = heatMap.G10.generate_gradiant(GRADIANT_SIZE)
        #####self.gradiant = self.gradiant.reshape((-1, 3))
gradiant = gradiant.reshape((-1, 3))
res = np.zeros((500, 640, 3), dtype=np.uint8)
depth_img = np.zeros(res.shape[:2], dtype=np.float32)
frame_idx = 0
pix_mm_depth = 0.34
step = 2

#db_Report = databaseManager("root", "dorsa-co", "localhost", "test_database")
#defect_tracker = defectTracker(min_g_thresh=20, step_per_line=2, db_Report=db_Report)



def defect_detection(frame_idx, fname,idx,defect_tracker):

    ###########################print("Idx on Defect Detection Page")
    ######################print(idx)    check whether idx recieve from LiveView_API page or not 
    # frame_idx = frame_idx = +1 
    #image_path = "Part6"
     ############################################      for getting image from folder    #############################
    #fpath = os.path.join(
    #    image_path, fname
    #) 

    #img = cv2.imread(
    #    fpath, 0
   # ) 
    #print("img.shapeeeeeeeeeeeeeeeee")
    #print(img)
    ################################### for getting image from camera             #######################################
    #img=fname
    if fname.ndim >2 :
            # img=cv2.
            fname = cv2.cvtColor(fname, cv2.COLOR_BGR2GRAY)
    #img = fname[:, 100:620]
    img = fname[:, 25:620]
    # -----------------------------------------------------------------------5
    #########################################      img = fname  ####################################  for getting image from camera
    # -----------------------------------------------------------------------
    img = cv2.blur(img, (5, 1))
    ###pts = ConvayerBase.extract_points(img, thresh=10, perspective_angle=60)  for previous version
    pts = ConvayerBase.extract_points(
                img,
                thresh=100,
                perspective_angle=60,
                min_tear_lenght=2,
                tear_depth=570
            )
   
    if len(pts) < 20:
                 pts = np.zeros((640, 2), dtype=np.int32)
                 pts[:, 0] = np.arange(0, len(pts))
                 pts[:, 1] = 618

       
    # -----------------------------------------------------------------------
    res_y = ConvayerBase.moving_avrage(pts[:, 1], 10)    #self.MOVING_AVRAGE=10
    pts = pts[: res_y.shape[0]]
    pts[:, 1] = res_y

            # -----------------------------------------------------------------------
            # tck = interpolate.splrep(pts[:,0], pts[:,1])
            # good_y = interpolate.splev(pts[:,0], tck).astype(np.int32)
    slope, intercept = linregress(pts)
    good_y = (pts[:, 0] * slope + intercept).astype(np.int32)

            # curve_parms,_ = curve_fit(curve_func, pts[:,0], pts[:,1])
            # good_y = curve_func(pts[:,0], *curve_parms)
    error_y = pts[:, 1] - good_y
  
    curve_parms, _ = curve_fit(
                curve_function,
                pts[abs(error_y) < 14][:, 0],
                pts[abs(error_y) < 14][:, 1],
    )
   
    good_y = curve_function(pts[:, 0], *curve_parms)
    error_y = pts[:, 1] - good_y
    error_y = pts[:, 1] - good_y
    error_y[abs(error_y) <= 2] = 0
    
    normalized_error_y = error_y / MAX_ERROR * GRADIANT_SIZE // 2
            # print(abs(error_y).max())
           
            # print(1/t)

    if frame_idx > res.shape[0] // step - step - 1:
                frame_idx = res.shape[0] // step -step - 1
                res[: -step] = res[step :]
                depth_img[: -step] = depth_img[step :]


    res[frame_idx * step : frame_idx * step + step,
                pts[:, 0],
            ] = gradiant[
                np.clip(
                    normalized_error_y + GRADIANT_SIZE // 2,
                    0,
                    GRADIANT_SIZE - 1,
                ).astype(np.int32)
            ]

    depth_img[
                frame_idx * step : frame_idx * step + step,
                pts[:, 0],
            ] = (
                error_y * pix_mm_depth
            )


            # max_depth=self.defect_tracker.get_defect_infoes(depth_img=self.depth_img,img=self.res)

    frame_idx += 1
    defect_tracker.refresh(
               res, depth_img=depth_img, Critical_Depth1=7    #Critical_Depth=10
            )
    res_draw = defect_tracker.draw(res)

    s = defect_tracker.function_inprogress_defects_cnts_x_y_w_h(
                depth_img=depth_img, img=res
            )
            #### s = self.defect_tracker.function_inprogress_defects_cnts_x_y_w_h()
    Number_Defect = defect_tracker.function_number_of_defect()
    Total_Area = defect_tracker.function_total_area_of_defect()
    Number_of_Critical_Defect = (
                defect_tracker.function_number_of_critical_defect()
    )


    #return res_draw, s, Number_Defect, Number_of_Critical_Defect,max_depth
    return res_draw, s, Number_Defect, Number_of_Critical_Defect


def function_total_complete_defects_cnts():
    all_cnts = defect_tracker.function_total_complete_defects_cnts()
    return all_cnts


def function_return_total_depth():
    total_depth_info = defect_tracker.function_return_total_depth()
    return total_depth_info


def function_return_critical_flage():
    critical_depth_flag = defect_tracker.function_return_critical_flage()
    return critical_depth_flag


def getDate():
    this_year = date.today().year
    this_month = date.today().month
    this_day = date.today().day
    str_date = jdatetime.date.fromgregorian(
        day=this_day, month=this_month, year=this_year
    )
    return str_date


def linregress(pts):
        x = np.expand_dims(pts[:, 0], axis=-1)
        y = np.expand_dims(pts[:, 1], axis=-1)
        featurs = np.hstack((np.ones_like(x), x))  # , x**2))
        theta = np.linalg.inv(np.matmul(featurs.transpose(), featurs))
        theta = np.matmul(theta, featurs.transpose())
        theta = np.matmul(theta, y)
        slope = theta[1]
        intercept = theta[0]
        return slope, intercept

def curve_function( x, a, b, c):
        return a * x**2 + b * x + c