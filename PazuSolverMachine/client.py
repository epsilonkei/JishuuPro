#!/usr/bin/python
#coding: utf-8

import socket

HOST = "157.82.7.54"  #サーバプログラムを動作させるホストを入力
#HOST = 'localhost'
PORT = 50008

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print 'Wait!'  #サーバ側の書き込みを待つ

while 1:
    data = s.recv(1024*8) #データの受信（1024バイトまで）
    list = data.split(' ')
    print '(server) >', list[0], list[1]
    data = raw_input('(client) > ') #クライアント側の入力
    s.send(data)          #ソケットに書き込む
    if data == "quit":    #quitが入力されたら終了
        break
s.close()
