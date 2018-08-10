#!/usr/bin/python
#coding: utf-8

import cv2
from get_map import *
from pazusolver import *
import time
#from machine import Machine
   
if __name__ == '__main__':
    """Capture video from camera"""
    # カメラをキャプチャする
    cap = cv2.VideoCapture(1) # 0はカメラのデバイス番号
    gamma = 0.75
    
    look_up_table = np.ones((256, 1), dtype = 'uint8' ) * 0
    for i in range(256):
        look_up_table[i][0] = 255 * pow(float(i) / 255, 1.0 / gamma)

    #machine = Machine()
    #machine.start()
    pre = []
    num_check = 5
    
    while True:
        # retは画像を取得成功フラグ
        ret, frame = cap.read()
        frame1 = cv2.LUT(frame, look_up_table)

        trim = trim_image(frame1)
        #for i in range(5):
        #    for j in range(6):
        #        cv2.circle(trim, (30+60*j, 30+60*i), 30, (0, 0, 255), 2)
        # フレームを表示する
        cv2.imshow('Camera capture', trim)
        
        _map = get_map(trim)
        map = Map(_map)
        map.count_combos()
        if map.num_combos == 0:
            if len(pre) == 0:
                pre.append(_map)
            elif np.array_equal(_map, pre[-1]):
                pre.append(_map)
                time.sleep(0.1)
            else:
                pre = [_map]
            if len(pre) >= num_check:
                '''Solve map'''
            
                print _map
                
                start_time=time.time()
                map.solve_map()
                map.ans()
                elapsed_time=time.time() - start_time
                print 'Elapsed time: ' + str(elapsed_time)

        
                '''Move Machine '''
                '''
                start, route, end = map.best_route() 
                machine.goto(start[0], start[1])
                machine.push()
                for di in route:
                    if di == 0:
                        machine.right()
                    elif di == 1:
                        machine.down()
                    elif di == 2:
                        machine.up()
                    elif di == 3:
                        machine.left()
                    
                machine.pull()        
                machine.back(end[0], end[1])
                '''
                break
        
        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            break
        
    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()

