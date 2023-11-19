import time
import numpy
cimport numpy
cimport cython
from libc.math cimport cos

cdef float pi = 3.14159


ctypedef numpy.int32_t DTYPE_int32
ctypedef numpy.uint8_t DTYPE_uint8
ctypedef numpy.float32_t DTYPE_float32

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def moving_avrage(numpy.ndarray[DTYPE_int32, ndim=1] arr, int window):   # This function is used to apply the moving-average function 

    cdef long int total
    cdef int i,w
    cdef int arr_shape = arr.shape[0]
    cdef numpy.ndarray[DTYPE_int32, ndim=1] res = numpy.zeros((arr_shape - window,), dtype = numpy.int32)
    #res = numpy.zeros((arr_shape - window,), dtype = numpy.int32 )

    for i in range(arr_shape - window):
        total = 0
        for w in range(window):
            total += arr[i+w]
        total = int(total / window)
        res[i] = total
    
    return res



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def moving_avrage_float(numpy.ndarray[DTYPE_float32, ndim=1] arr, int window):

    cdef float total
    cdef int i,w
    cdef int arr_shape = arr.shape[0]
    cdef numpy.ndarray[DTYPE_float32, ndim=1] res = numpy.zeros((arr_shape - window,), dtype = numpy.float32)
    #res = numpy.zeros((arr_shape - window,), dtype = numpy.int32 )

    for i in range(arr_shape - window):
        total = 0
        for w in range(window):
            total += arr[i+w]
        total = total / window
        res[i] = total
    
    return res


@cython.boundscheck(False)
@cython.wraparound(False)
def extract_points(numpy.ndarray[DTYPE_uint8, ndim=2] img, int thresh, int perspective_angle,int min_tear_lenght, int tear_depth):  

    cdef long long int total_sum
    cdef int total_count, last_j
    cdef int i,j,k
    cdef int point_idx = 0
    cdef int img_h = img.shape[0]
    cdef int img_w = img.shape[1]
    cdef int start_tear_x = 0
    cdef int is_tear = 0
    cdef numpy.ndarray[DTYPE_int32, ndim=2] res_pts = numpy.zeros( (img_w, 2), dtype = numpy.int32 ) 
    cdef float perspective = cos(perspective_angle * pi / 180)     

    for i in range(img_w):
        total_sum = 0
        total_count = 0
        for j in range(img_h):
            if img[j,i] > thresh:
                
                # remove noise 
                if total_count>0 and total_count<3 and j - last_j > 5:
                    total_count = 1
                    total_sum = j
                    last_j = j
                else:
                    total_count += 1
                    total_sum += j
                    last_j = j
        
        
        if total_count>0:
            if is_tear == 1:
                is_tear = 0
                if i - start_tear_x > min_tear_lenght:
                    for k in range(start_tear_x, i):
                        res_pts[point_idx,0] = k
                        res_pts[point_idx,1] = tear_depth
                        point_idx+=1
                    
 
            res_pts[point_idx,0] = i
            res_pts[point_idx,1] = int((total_sum / total_count) / perspective + 0.01 )
            #print(total_sum, total_count, res_pts[point_idx,1], int((total_sum / total_count)))
            point_idx+=1

            
                
        else:
            if is_tear == 0:
                is_tear = 1
                start_tear_x = i




    
    return res_pts[:point_idx]






@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def calc_slope(numpy.ndarray[DTYPE_int32, ndim=2] arr, int step):   # This function is used to calculate slope for the input array

    cdef float slope
    cdef int i = 0
    cdef int arr_shape = arr.shape[0]
    cdef numpy.ndarray[DTYPE_float32, ndim=1] res = numpy.zeros((arr_shape - step,), dtype = numpy.float32)

    for i in range(arr_shape - step):
        slope = ( arr[ i + step, 1] - arr[i, 1] ) / (( arr[ i + step, 0] - arr[i ,0] ) + 0.001 ) 
        #res[i,0] = arr[i,0]
        #slope = ( 3*arr[ i-3, 1]+3*arr[ i-2, 1]-4*arr[i-1, 1] -4*arr[ i , 1] -4*arr[ i+1, 1]+3*arr[ i+2, 1]+3*arr[i+3, 1] ) / (( 3*arr[ i-3, 0]+3*arr[ i-2, 0]-4*arr[i-1, 0] -4*arr[ i , 0] -4*arr[ i+1,0]+3*arr[ i+2, 0]+3*arr[i+3, 0] ) + 0.001 ) 
        res[i] = slope
        print(slope)
        

    return res



@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def find_boundary_of_defect(numpy.ndarray[DTYPE_int32, ndim=2] depths_pts, int min_gap, int min_defect_depth, int margin,int min_defect_lenght,):   # This function is used to calculate slope for the input array
    #depths_pts [[x1,y1],[x2,y2],..]
    
    cdef int i = 0
    cdef int buffer_end_boundary = 0
    cdef int buffer_start_boundary = 0
    cdef int gap = 0  # This is used to store the gap between two consecutive defects
    cdef int flag_start_end = 0
    cdef int idx_boundary_defect = 0
    cdef int n = depths_pts.shape[0]
    cdef numpy.ndarray[DTYPE_int32, ndim=2] boundary_points = numpy.zeros((100,2), dtype = numpy.int32)
    cdef int max_x = numpy.max(depths_pts[:,0])
    for i in range(n):
        
        if numpy.abs(depths_pts[i][1]) >= min_defect_depth :
              gap=0
              if flag_start_end == 0: # Find the start of the defect 
                 buffer_start_boundary = depths_pts[i,0]
                 flag_start_end=1
                 #print("if1")

              if flag_start_end == 2:
                 flag_start_end=1
                #print("if2")
            
        else:
            gap=gap+1
            if flag_start_end == 1:  # Find the candidate of the end of the defect
                 buffer_end_boundary = depths_pts[i,0]
                 flag_start_end=2
                 #print("if3")
       
            if    flag_start_end  ==2 and gap> min_gap :  
                # Check whether the last candidate is true or not , 
                #the distance between the next and previous 
                #defect must be more than min_gap 
                if buffer_end_boundary - buffer_start_boundary > min_defect_lenght:
                    buffer_end_boundary += margin
                    buffer_start_boundary -= margin
                    if buffer_start_boundary< 0:
                        buffer_start_boundary = 0
                    if buffer_end_boundary > max_x:
                        buffer_end_boundary = max_x
                    boundary_points[idx_boundary_defect,1]=buffer_end_boundary
                    boundary_points[idx_boundary_defect,0]=buffer_start_boundary
                    flag_start_end=0
                    idx_boundary_defect=idx_boundary_defect+1 #    Number of defect
                else:
                    flag_start_end=0
                 #print("if")

        #print(depths_pts[i], gap)
    if  idx_boundary_defect >0 :
        return boundary_points[0:idx_boundary_defect]
    else :  
        return numpy.array([],dtype=numpy.int32)



        

    

