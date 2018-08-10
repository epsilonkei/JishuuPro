import cv2
import numpy as np

img = cv2.imread('image.jpg')
cv2.namedWindow('image')

def draw_frame(img):
    for i in range(6):
        for j in range(5):
            cv2.rectangle(img, (15+60*i, 15+60*j), (45+60*i, 45+60*j), (255,0,0), 2) 
    return img

while(1):
    img = draw_frame(img)
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
