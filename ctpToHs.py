# -*- coding: utf-8 -*-
import xdrlib ,sys
import xlrd
import copy
import xlwt
import csv
import os
from datetime import *
from kingNew import *
import io
#把datetime转成字符串
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d-%H")

#把字符串转成datetime
def string_toDatetime(string):
    return datetime.strptime(string, "%Y%m%d")

#把字符串转成时间戳形式
def string_toTimestamp(strTime):
    return time.mktime(string_toDatetime(strTime).timetuple())

#把时间戳转成字符串形式
def timestamp_toString(stamp):
    return time.strftime("%Y-%m-%d-%H", time.localtime(stamp))

#把datetime类型转外时间戳形式
def datetime_toTimestamp(dateTim):
    return time.mktime(dateTim.timetuple())


def readBill(path):
    blockList = []
    files = os.listdir(path)
    file = path + '/' + files[0]
    if not os.path.isfile(file):
        return
    with open(file, 'r') as srcFile:
        textlist = srcFile.readlines()
    srcFile.close()
    return textlist
def readBill_first(path):
    files = os.listdir(path)
    file = path + '/' + files[0]
    if not os.path.isfile(file):
        return
    file_object = open(file)
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )
    return all_the_text
def readBill_All(path):
    files = os.listdir(path)
    textContainer = []
    for file in files:
        file = path + '/' + file
        if not os.path.isfile(file):
            continue
        if file.endswith('txt'):
            with open(file, 'r') as srcFile:
                text = srcFile.readlines()
            textContainer.append(text)
            srcFile.close()

    return textContainer

def processBill(text):

    return
def main():

    path = './txt'
    subAccPath = './subacc';
    presentCTPBill = './presentCTPBill'
    #subAccPath = presentCTPBill

    textContainer = readBill_All(subAccPath)
    for text in textContainer:
        tempKN = kingNew(text)
        tempKN.clear();
        del tempKN



    print("\n程序运行正常结束！")
    return

if __name__=="__main__":
    main()
