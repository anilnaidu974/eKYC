import traceback
import cv2
import numpy as np
import math
import datetime
import os


GESTURE_ROI = os.path.join(os.getcwd(),"database/gesture_roi")
def getGestureNumber(imagePath):
    try:  #an error comes if it does not find anything in window as it cannot find contour of max area
            #therefore this try error statement
            
        # ret, frame = cap.read()
        frame = cv2.imread(imagePath)
        
        print("****************************",frame.shape)
        kernel = np.ones((3,3),np.uint8)
        
        #define region of interest
        # roi=frame[200:500, 200:500]
        # roi=frame[0:300, 200:600]
        # roi=frame[150:300, 435:640]
        roi=frame[200:450, 850:1230]
        current_datetime = datetime.datetime.now()
        gesture_roi_path = os.path.join(GESTURE_ROI, str(current_datetime) + "_roi.png")
        cv2.imwrite(gesture_roi_path,roi)
        
        
    
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        
            
    # define range of skin color in HSV
        lower_skin = np.array([0,20,70], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)
        
        #extract skin colur imagw  
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        

        
    #extrapolate the hand to fill dark spots within
        mask = cv2.dilate(mask,kernel,iterations = 4)
        
    #blur the image
        mask = cv2.GaussianBlur(mask,(5,5),100) 
        
    #find contours
        contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
        
    #find contour of max area(hand)
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
        
    #approx the contour a little
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx= cv2.approxPolyDP(cnt,epsilon,True)
        
        
    #make convex hull around hand
        hull = cv2.convexHull(cnt)
        
        #define area of hull and area of hand
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
        
    #find the percentage of area not covered by hand in convex hull
        arearatio=((areahull-areacnt)/areacnt)*100

        #find the defects in convex hull with respect to hand
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)
        
    # l = no. of defects
        l=0
        
    #code for finding no. of defects due to fingers
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            pt= (100,180)
            
            
            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            
            #distance between point and convex hull
            d=(2*ar)/a
            
            # apply cosine rule here
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
        
            # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
            if angle <= 90 and d>30:
                l += 1
                cv2.circle(roi, far, 3, [255,0,0], -1)
            
            #draw lines around hand
            cv2.line(roi,start, end, [0,255,0], 2)
            
            
        l+=1
        # print("**************************** : ",l)
        return l
        
    except Exception:
        traceback.print_exc()
        pass
    # break
        
    
