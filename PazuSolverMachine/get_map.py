import cv2
import numpy as np

def trim_image(img):
    pts1 = np.float32([[298,215], [487,213], [296,365], [508,367]])
    pts2 = np.float32([[0,0],[360,0],[0,300],[360,300]])
    
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(360,300))
    return dst

def detect_red_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # color mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    
    return mask

def detect_yellow_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color mask (170-180)
    lower_red = np.array([30,50,50])
    upper_red = np.array([50,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)

    return mask

def detect_green_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color mask (170-180)
    lower_red = np.array([70,50,50])
    upper_red = np.array([90,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    
    return mask

def detect_blue_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color mask (170-180)
    lower_red = np.array([95,50,50])
    upper_red = np.array([110,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    
    return mask
   
def detect_pink_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color mask (170-180)
    lower_red = np.array([140,50,50])
    upper_red = np.array([155,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    
    return mask

def detect_violet_color(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color mask (170-180)
    lower_red = np.array([120,50,50])
    upper_red = np.array([132,255,255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    
    return mask

def get_map(img):
    #img1 = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
    mask = []
    mask.append(detect_red_color(img))
    mask.append(detect_yellow_color(img))
    mask.append(detect_green_color(img))
    mask.append(detect_blue_color(img))
    mask.append(detect_pink_color(img))
    mask.append(detect_violet_color(img))
    mask = np.array(mask)
    
    map = np.zeros((5,6), dtype = np.int)
    for i in range(5):
        for j in range(6):
            map[i,j]= np.argmax(np.sum(mask[:,(25+60*i):(36+60*i),(25+60*j):(36+60*j)], axis=(1,2)))

    return map    
            
if __name__ == "__main__":
    img_files = 'img20170110-191855.jpg'
    img = cv2.imread(img_files)
    dst = trim_image(img)
    map = get_map(dst)
    print map
