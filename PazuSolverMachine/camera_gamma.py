#!/usr/bin/python
#coding: utf-8

import cv2
from get_map import *
from pazusolver import *
import numpy as np
   
if __name__ == '__main__':
    """Capture video from camera"""
    # カメラをキャプチャする
    cap = cv2.VideoCapture(1) # 0はカメラのデバイス番号
    # ガンマ定数の定義
    gamma = 0.75
    
    look_up_table = np.ones((256, 1), dtype = 'uint8' ) * 0
    for i in range(256):
        look_up_table[i][0] = 255 * pow(float(i) / 255, 1.0 / gamma)

    while True:
        # retは画像を取得成功フラグ
        ret, frame = cap.read()
        # ガンマ変換後の出力
        frame1 = cv2.LUT(frame, look_up_table)
        
        trim = trim_image(frame1)
        # -*- coding: utf-8 -*-

        for i in range(5):
            for j in range(6):
                cv2.circle(trim, (30+60*j, 30+60*i), 30, (0, 0, 255), 2)
        # フレームを表示する
        cv2.imshow('Camera capture', trim)
        
        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            break
        
    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()

