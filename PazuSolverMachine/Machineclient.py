s#!/usr/bin/python
#coding: utf-8

import socket
from machine import Machine

HOST = "192.168.11.5"  #サーバプログラムを動作させるホストを入力
#HOST = 'localhost'
PORT = 50007

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print 'Wait!'  #サーバ側の書き込みを待つ
    
    while 1:
        data = s.recv(1024*8) #データの受信（1024バイトまで）
        print '(server) >', data
        list = data.split(' ')
        print '(server) >', data
        list = map(int, list)
        start = [data[0], data[1]]
        end = [data[2], data[3]]
        route = data[4:]
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
        
        data2 = 'Done'
        s.send(data2)          #ソケットに書き込む
        if data == "quit":    #quitが入力されたら終了
        break
    s.close()

