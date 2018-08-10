#! /usr/bin/python
# coding: utf-8
 
import glob
import numpy as np
import cv2
 
def thres(image_file):
    im = cv2.imread(image_file, 0) 
    str_time = image_file[12:]
    th = cv2.threshold(im, 0, 255, cv2.THRESH_OTSU)[1]
    cv2.imwrite('./ThresData/'+str_time, th)
    
if __name__ == '__main__':
    # パス内の全ての"指定パス+ファイル名"と"指定パス+ディレクトリ名"を要素とするリストを返す
    files = glob.glob('./TrainData/*/*.jpg') # ワイルドカードが使用可能
 
    for file in files:
        thres(file)
