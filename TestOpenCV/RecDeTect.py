#! /usr/bin/python
# coding: utf-8

import numpy as np
import cv2

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)

    while cv2.waitKey(10) == -1:
        orig = cam.read()[1]
        im = orig.copy()
        
        # Gray scale
        #imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        # 2値化
        #ret,thresh = cv2.threshold(imgray, 128, 255, cv2.THRESH_OTSU)
        # 輪郭を抽出する
        canny = cv2.cvtColor(orig, cv2.cv.CV_BGR2GRAY)
        canny = cv2.GaussianBlur(canny, (5, 5), 0)
        canny = cv2.Canny(canny, 50, 100)
        # 輪郭検出 
        contours, hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #輪郭描画
        cv2.drawContours(im, contours, -1, (0,255,0), 3)
        cv2.imshow("Original Image", orig)
        cv2.imshow("Contours",im)

    cam.release()
    cv2.destroyAllWindows()
