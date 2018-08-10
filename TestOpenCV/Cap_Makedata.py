#! /usr/bin/python
# coding: utf-8

import numpy as np
import cv2

image_file = 'capture.jpg'

def getPartImageByRect(img, points):
    points = list(map(lambda x: x[0], points))
    points = sorted(points, key=lambda x:x[1])
    top_points = sorted(points[:2], key=lambda x:x[0])
    bottom_points = sorted(points[2:4], key=lambda x:x[0])
    points = top_points + bottom_points

    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[500,0],[0,300],[500,300]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    
    dst = cv2.warpPerspective(img,M,(500,300))
    return dst

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

    th = (th1 + th2 + th3 + th4)/4
    im_th = cv2.threshold(th, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    
    contours = cv2.findContours(im_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]

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
        trim = getPartImageByRect(im, approx)
        cv2.imwrite('./out/output'+str(i)+'.jpg', trim)
        #block1 = trim[20:75, 205:260]
        for j in range(4):
            for k in range(4):
                block = trim[(19+68*(3-j)):(74+68*(3-j)),(205+68*k):(260+68*k)]
                cv2.imwrite('./out/block'+str(i)+str(j)+str(k)+'.jpg', block)
    
