#! /usr/bin/python
# coding: utf-8

import numpy as np
import cv2

image_file = 'capture.jpg'

def getRectByPoints(points):
    #print np.float32(points)
    #print np.float32([[0,0],[500,0],[0,300],[500,300]])
    # prepare simple array 
    points = list(map(lambda x: x[0], points))
    #print np.float32(points)
    points = sorted(points, key=lambda x:x[1])
    #print np.float32(points)
    top_points = sorted(points[:2], key=lambda x:x[0])
    bottom_points = sorted(points[2:4], key=lambda x:x[0])
    points = top_points + bottom_points
    #print points

    left = min(points[0][0], points[2][0])
    right = max(points[1][0], points[3][0])
    top = min(points[0][1], points[1][1])
    bottom = max(points[2][1], points[3][1])
    #print (top, bottom, left, right)
    return (top, bottom, left, right)

def getPartImageByRect(rect):
    img = cv2.imread(image_file, 1)
    print rect
    imgs = img[rect[0]:rect[1], rect[2]:rect[3]]
    return imgs

if __name__ == '__main__':
    im = cv2.imread(image_file, 1) 
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
    im_blur = cv2.GaussianBlur(im_gray, (11, 11), 0)
    th1 = cv2.threshold(im_blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    
    imr_blur = cv2.GaussianBlur(im[:,:,2], (11, 11), 0)
    th2 = cv2.threshold(imr_blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    img_blur = cv2.GaussianBlur(im[:,:,1], (11, 11), 0)
    th3 = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    imb_blur = cv2.GaussianBlur(im[:,:,0], (11, 11), 0)
    th4 = cv2.threshold(imb_blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    #ima = np.abs(im[:,:,2] - im[:,:,1]) + np.abs(im[:,:,2] - im[:,:,0])
    #ima_blur = cv2.GaussianBlur(ima, (11, 11), 0)
    #th5 = cv2.threshold(ima_blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    th = (th1 + th2 + th3 + th4)/4
    im_th = cv2.threshold(th, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    
    contours = cv2.findContours(im_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]
    #cv2.drawContours(im, contours, -1, (0,255,0), 3)

    # filtered with area over (all area / 100 )
    th_area = im.shape[0] * im.shape[1] /10
    contours_large = list(filter(lambda c:cv2.contourArea(c) > th_area, contours))
    
    outputs = []
    rects = []
    approxes = []
    
    for (i,cnt) in enumerate(contours_large):
        arclen = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.1*arclen, True)
        if len(approx) < 4:
            continue
        approxes.append(approx)
        rect = getRectByPoints(approx)
        rects.append(rect)
        outputs.append(getPartImageByRect(rect))
        cv2.imwrite('./out1/output'+str(i)+'.jpg', getPartImageByRect(rect))
        #cv2.imwrite('./out/output'+str(i)+'.jpg', getPartImageByRect(approx))

    
    #cv2.imshow("Contours", im)
    #cv2.imwrite('capture_th.jpg', im_th)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
