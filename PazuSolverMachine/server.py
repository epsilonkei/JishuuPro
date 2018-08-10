#!/usr/bin/python
#coding: utf-8

import socket

HOST = "192.168.11.5"   #サーバプログラムを動作させるホストを入力
#HOST = 'localhost'
PORT = 50007         #接続するポート番号指定
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) #サーバのアドレスをソケットに設定
s.listen(1)          #１つの接続要求を待つ
soc, addr = s.accept() #要求が来るまでブロックする
print 'Conneted by', addr
print 'Go ahead!'  #サーバ側から先に書き込む

while 1:
    #data = raw_input('(server) > ') #サーバ側の入力
    data = str(1) + ' '+ str(2)
    soc.send(data) #ソケットに書き込む
    data = soc.recv(1024*8) #1024バイトまでのデータを受け取る
    print '(client) >',data
    if data == "quit": #quitが入力されたら終了
        break
soc.close()
