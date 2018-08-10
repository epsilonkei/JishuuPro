#! /usr/bin/python
# coding: utf-8
 
import glob
 
# パス内の全ての"指定パス+ファイル名"と"指定パス+ディレクトリ名"を要素とするリストを返す
files = glob.glob('./TrainData/*/*.jpg') # ワイルドカードが使用可能
 
for file in files:
    print int(file[12:14])
