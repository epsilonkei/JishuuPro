import cv2
import numpy as np

# mouse callback function
def print_coord(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print x,y

# Create a black image, a window and bind the function to window
img = cv2.imread('image.jpg')
cv2.namedWindow('image')
cv2.setMouseCallback('image',print_coord)

while(1):
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
