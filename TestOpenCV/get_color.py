import cv2
import numpy as np

img_files = 'img20170108-111442.jpg'
img = cv2.imread(img_files)
pts1 = np.float32([[298,215], [487,213], [296,365], [508,367]])
pts2 = np.float32([[0,0],[400,0],[0,300],[400,300]])

M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,M,(400,300))
    
def detect_red_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
    
    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
    
    # join my masks
    mask = mask1 
    
    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    
    # or your HSV image, which I *believe* is what you want
    output_hsv = img_hsv.copy()
    output_hsv[np.where(mask==0)] = 0
    return output_img

def detect_yellow_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color mask (170-180)
    lower_red = np.array([10,50,50])
    upper_red = np.array([50,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    
    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    
    return output_img

def detect_green_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color mask (170-180)
    lower_red = np.array([60,50,50])
    upper_red = np.array([90,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    
    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    
    return output_img

def detect_blue_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color mask (170-180)
    lower_red = np.array([95,50,50])
    upper_red = np.array([110,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    
    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    
    return output_img
   
def detect_pink_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color mask (170-180)
    lower_red = np.array([150,50,50])
    upper_red = np.array([160,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    
    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    
    return output_img

def detect_violet_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color mask (170-180)
    lower_red = np.array([120,50,50])
    upper_red = np.array([140,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    
    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    
    return output_img
 
while(1):
    output_img = detect_red_color(dst)
    cv2.imshow('red',output_img)
    output_img = detect_yellow_color(dst)
    cv2.imshow('yellow',output_img)
    output_img = detect_green_color(dst)
    cv2.imshow('green',output_img)
    output_img = detect_blue_color(dst)
    cv2.imshow('blue',output_img)
    output_img = detect_pink_color(dst)
    cv2.imshow('pink',output_img)
    output_img = detect_violet_color(dst)
    cv2.imshow('violet',output_img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
