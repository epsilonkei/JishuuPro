#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wiringpi as wp
import time
import struct
import signal

L6470_SPI_SPEED         = 1000000
STEPPING_TICK           = 200

# BUSY PIN の設定
BUSY_PIN_0      = 21
BUSY_PIN_1      = 20
io = wp.GPIO(wp.GPIO.WPI_MODE_GPIO)
io.pinMode(BUSY_PIN_0,io.INPUT)


def exit_handler(signal, frame):
    # Ctrl+Cが押されたときにデバイスを初期状態に戻して終了する。
    print("\nExit")
    L6470_softstop(0)
    #L6470_softstop(1)
    L6470_softhiz(0)
    #L6470_softhiz(1)
    quit()

# 終了処理用のシグナルハンドラを準備
signal.signal(signal.SIGINT, exit_handler)

def L6470_write(channel, data):
    data = struct.pack("B", data)
    return wp.wiringPiSPIDataRW(channel, data)
    
def L6470_init(channel):
    # MAX_SPEED設定。
    # レジスタアドレス。
    L6470_write(channel, 0x07)
    # 最大回転スピード値(10bit) 初期値は 0x41
    L6470_write(channel, 0x00)
    L6470_write(channel, 0x27)
    
    # KVAL_HOLD設定。
    # レジスタアドレス。
    L6470_write(channel, 0x09)
    # モータ停止中の電圧設定(8bit) 初期値は 0x29
    L6470_write(channel, 0x29)
    
    # KVAL_RUN設定。
    # レジスタアドレス。
    L6470_write(channel, 0x0A)
    # モータ定速回転中の電圧設定(8bit) 初期値は 0x29
    L6470_write(channel, 0x80)
    
    # KVAL_ACC設定。
    # レジスタアドレス。
    L6470_write(channel, 0x0B)
    # モータ加速中の電圧設定(8bit) 初期値は 0x29
    L6470_write(channel, 0x80)
    
    # KVAL_DEC設定。
    # レジスタアドレス。
    L6470_write(channel, 0x0C)
    # モータ減速中の電圧設定(8bit) 初期値は 0x8A
    L6470_write(channel, 0xFF)

    # OCD_TH設定。
    # レジスタアドレス。
    L6470_write(channel, 0x13)
    # オーバーカレントスレッショルド設定(4bit)
    L6470_write(channel, 0x0F)
    
    # STALL_TH設定。
    # レジスタアドレス。
    L6470_write(channel, 0x14)
    # ストール電流スレッショルド設定(4bit)
    L6470_write(channel, 0x7F)
    
    # STEP_MODE 設定。
    # レジスタアドレス。
    L6470_write(channel, 0x16)
    # sTEP_MODE設定(8bit) 初期値は 0x07(1/128)
    #L6470_write(channel, 0x07)
    L6470_write(channel, 0x00)

def L6470_run(channel, speed):
    # 方向検出。
    if (speed < 0):
        dir = 0x50
        spd = -1 * speed
    else:
        dir = 0x51
        spd = speed
        
    # 送信バイトデータ生成。
    spd_h   = (0x0F0000 & spd) >> 16 
    spd_m   = (0x00FF00 & spd) >> 8 
    spd_l   = (0x0000FF & spd) 
    
    # コマンド（レジスタアドレス）送信。
    L6470_write(channel, dir)
    # データ送信。
    L6470_write(channel, spd_h)
    L6470_write(channel, spd_m)
    L6470_write(channel, spd_l)
    
def L6470_move(channel, n_step):
    # 方向検出。
    if (n_step < 0):
        dir = 0x40
        stp = -1 * n_step
    else:
        dir = 0x41
        stp = n_step

    # 送信バイトデータ生成。
    stp_h   = (0x3F0000 & stp) >> 16 
    stp_m   = (0x00FF00 & stp) >> 8 
    stp_l   = (0x0000FF & stp) 
    
    # コマンド（レジスタアドレス）送信。
    L6470_write(channel, dir)
    # データ送信。
    L6470_write(channel, stp_h)
    L6470_write(channel, stp_m)
    L6470_write(channel, stp_l)
    '''
    if channel == 0:
        pin     = BUSY_PIN_0
    else:
        pin     = BUSY_PIN_1
    while( io.digitalRead(pin) == 0 ):
        pass
    '''
   
def L6470_softstop(channel):
    print("***** SoftStop. *****")
    dir = 0xB0
    # コマンド（レジスタアドレス）送信。
    L6470_write(channel, dir)
    '''
    if channel == 0:
        pin     = BUSY_PIN_0
    else:
        pin     = BUSY_PIN_1
    while( io.digitalRead(pin) == 0 ):
        pass
    '''
 
def L6470_softhiz(channel):
    print("***** Softhiz. *****")
    dir = 0xA8
    # コマンド（レジスタアドレス）送信。
    L6470_write(channel, dir)
    '''
    if channel == 0:
        pin     = BUSY_PIN_0
    else:
        pin     = BUSY_PIN_1
    while( io.digitalRead(pin) == 0 ):
        pass
    '''

def L6470_getstatus(channel):
    print("***** Getstatus. *****")
    dir = 0xD0
    # コマンド（レジスタアドレス）送信。
    print L6470_write(channel, dir)
    time.sleep(0.2)
    
if __name__=="__main__":
    speed = 0
    
    print("***** start spi test program *****")
    
    # SPI channel を L6470_SPI_SPEED で開始。
    wp.wiringPiSPISetup (0, L6470_SPI_SPEED)
    #wp.wiringPiSPISetup (1, L6470_SPI_SPEED)
    
    # L6470の初期化。
    L6470_init(0)
    #L6470_init(1)
    
    L6470_move(0, -200)
    #L6470_move(1, -200)
    #L6470_move(0, 800)
    #L6470_move(1, -100)
    #L6470_move(0, 100)
    #L6470_move(1, -200)
    #L6470_softstop(0)
    #L6470_softstop(1)
    
    #L6470_run(0, 30000)
    #L6470_run(1, -30000)
    #time.sleep(2)
    
    #L6470_softstop(0)
    #L6470_softstop(1)
    #L6470_softhiz(0)
    #L6470_softhiz(1)
    quit()
