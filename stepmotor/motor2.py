#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wiringpi as wp
import time
import struct

L6470_SPI_CHANNEL       = 0
L6470_SPI_SPEED         = 1000000
STEPPING_TICK           = 200

def L6470_write(data):
  data = struct.pack("B", data)
  wp.wiringPiSPIDataRW(L6470_SPI_CHANNEL, data)

def L6470_init():
  # MAX_SPEED設定。
  # レジスタアドレス。
  L6470_write(0x07)
  # 最大回転スピード値(10bit) 初期値は 0x41
  L6470_write(0x00)
  L6470_write(0x41)
  
  # KVAL_HOLD設定。
  # レジスタアドレス。
  L6470_write(0x09)
  # モータ停止中の電圧設定(8bit)
  L6470_write(0xFF)
  
  # KVAL_RUN設定。
  # レジスタアドレス。
  L6470_write(0x0A)
  # モータ定速回転中の電圧設定(8bit)
  L6470_write(0xFF)
  
  # KVAL_ACC設定。
  # レジスタアドレス。
  L6470_write(0x0B)
  # モータ加速中の電圧設定(8bit)
  L6470_write(0xFF)
  
  # KVAL_DEC設定。
  # レジスタアドレス。
  L6470_write(0x0C)
  # モータ減速中の電圧設定(8bit) 初期値は 0x8A
  L6470_write(0x40)
  
  # OCD_TH設定。
  # レジスタアドレス。
  L6470_write(0x13)
  # オーバーカレントスレッショルド設定(4bit)
  L6470_write(0x0F)
  
  # STALL_TH設定。
  # レジスタアドレス。
  L6470_write(0x14)
  # ストール電流スレッショルド設定(4bit)
  L6470_write(0x7F)
  
def L6470_move(step):
  # 方向検出。
  if (step < 0):
    dir = 0x40
    n_step = -1 * step
  else:
    dir = 0x41
    n_step = step
    
  # 送信バイトデータ生成。
  n_step_1   =  (0x3F0000 & n_step) >> 16 
  n_step_2   =  (0x00FF00 & n_step) >> 8 
  n_step_3   =  (0x0000FF & n_step) 

  # コマンド（レジスタアドレス）送信。
  L6470_write(dir)
  # データ送信。
  L6470_write(n_step_1)
  L6470_write(n_step_2)
  L6470_write(n_step_3)

def L6470_softstop():
  print("***** SoftStop. *****")
  dir = 0xB0
  # コマンド（レジスタアドレス）送信。
  L6470_write(dir)
  time.sleep(1)

def L6470_softhiz():
  print("***** Softhiz. *****")
  dir = 0xA8
  # コマンド（レジスタアドレス）送信。
  L6470_write(dir)
  time.sleep(1)
  
if __name__=="__main__":
  print("***** start spi test program *****")
  
  # SPI channel 0 を 1MHz で開始。
  #wp.wiringPiSetupGpio()
  wp.wiringPiSPISetup (L6470_SPI_CHANNEL, L6470_SPI_SPEED)
  
  # L6470の初期化。
  L6470_init()
  
  while True:
    for i in range (10):
      L6470_move(4000)
      time.sleep(0.1)

    #L6470_softstop()
    #L6470_softhiz()
    quit()
  quit()
