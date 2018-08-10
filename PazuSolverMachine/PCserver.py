#!/usr/bin/python
#coding: utf-8

import socket
import cv2
from get_map import *
from pazusolver import *
import time

HOST = "10.10.1.64"   #サーバプログラムを動作させるホストを入力
#HOST = "192.168.11.5"
#HOST = 'localhost'
PORT = 50007         #接続するポート番号指定

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT)) #サーバのアドレスをソケットに設定
    s.listen(1)          #１つの接続要求を待つ
    soc, addr = s.accept() #要求が来るまでブロックする
    print 'Conneted by', addr
    print 'PC ready!'  #サーバ側から先に書き込む
    """Capture video from camera"""
    cap = cv2.VideoCapture(1)  
    gamma = 0.75
    
    look_up_table = np.ones((256, 1), dtype = 'uint8' ) * 0
    for i in range(256):
        look_up_table[i][0] = 255 * pow(float(i) / 255, 1.0 / gamma)
    pre = []
    num_check = 5

    while 1:
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
                # Solve map
                print _map
                start_time=time.time()
                map.solve_map()
                map.ans()
                elapsed_time=time.time() - start_time
                print 'Elapsed time: ' + str(elapsed_time)
                
                # Send route
                start, route, end = map.best_route()
                data = str(start[0])+' '+str(start[1])+' '+str(end[0])+' '+str(end[1])
                for di in route:
                    data += ' '+str(di)
                soc.send(data) #ソケットに書き込む
                data = soc.recv(1024*8) #1024バイトまでのデータを受け取る
                print '(client) >',data                
                break

        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            break

        #data = raw_input('(server) > ') #サーバ側の入力
        #data = str(1) + ' '+ str(2)
        #soc.send(data) #ソケットに書き込む
        #data = soc.recv(1024*8) #1024バイトまでのデータを受け取る
        #print '(client) >',data
        #if data == "quit": #quitが入力されたら終了
        #    break
    
    soc.close()
    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()
