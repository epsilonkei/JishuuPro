import cv2
import cv2.cv as cv
import numpy as np

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)

    while cv2.waitKey(10) == -1:
        orig = cam.read()[1]
        img = cv2.cvtColor(orig, cv2.cv.CV_BGR2GRAY)
        img = cv2.medianBlur(img,5)
        #img = cv2.GaussianBlur(img,(5,5),0)
        cimg = img
        #cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        
        circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,20,
                                   param1=50,param2=30,minRadius=0,maxRadius=0)
        
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

        cv2.imshow('detected circles',cimg)
    
    cam.release()
    cv2.destroyAllWindows()
