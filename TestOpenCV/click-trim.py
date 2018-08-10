import cv2
import numpy as np

# mouse callback function
def print_coord(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print x,y

# Create a black image, a window and bind the function to window
img = cv2.imread('img20170108-005145.jpg')
cv2.namedWindow('image')
cv2.setMouseCallback('image',print_coord)

while(1):
    pts1 = np.float32([[298,215], [487,213], [296,365], [508,367]])
    pts2 = np.float32([[0,0],[360,0],[0,300],[360,300]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    
    dst = cv2.warpPerspective(img,M,(360,300))
    
    cv2.imshow('image',dst)
    if cv2.waitKey(20) & 0xFF == 27:
        break
    cv2.imwrite('image.jpg',dst)
cv2.destroyAllWindows()
