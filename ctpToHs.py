# -*- coding: utf-8 -*-
import xdrlib ,sys
import copy
import os
from datetime import *
from kingNew import *
from aggregateFutures import *
from KingNewSchema import *
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

#need read gbk txt error
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
#need read gbk txt error
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
#bug fixed read gbk txt error
def readBill_All(path):
    files = os.listdir(path)
    textContainer = []
    for file in files:
        file = path + '/' + file
        if not os.path.isfile(file):
            continue
        if file.endswith('txt'):
            with open(file, 'rb') as srcFile:
                #content = fp.read().decode('utf-8')
                content = srcFile.read().decode('utf-8')
                # for oneline in content:
                #     oneline.decode('utf-8')
                #content = content.strip('\r')
                text = content.split('\n')


                #text = srcFile.readlines()
            textContainer.append(text)
            srcFile.close()

    return textContainer

def processBill(text):

    return

def aggregate(textContainer = []):
    global positions
    allPositions = []
    for text in textContainer:
        tempAgg = aggregateFutures(text)
        tPostions = tempAgg.getPositions()
        allPositions.append(tPostions)

    parse = '__________________________________________________________________________'

    setDet = {}

    for eachPosition in allPositions:
        print(parse)
        for node in eachPosition:
            #print(node)
            if node[positions['Instrument']] not in setDet:
                tempAgNode = {}
                tempAgNode['卖'] = 0
                tempAgNode['买'] = 0
                tempAgNode['卖成交价'] = 0
                tempAgNode['买成交价'] = 0
                tempAgNode['持仓盯市盈亏'] = 0
                tempAgNode['卖保证金占用'] = 0
                tempAgNode['买保证金占用'] = 0
                if '买' in node[positions['B/S']]:
                    tempAgNode['买'] = int(node[positions['Lots']])
                    tempAgNode['买成交价'] = Decimal(node[positions['AvgOpenPrice']])
                    tempAgNode['买保证金占用'] = Decimal(node[positions['MarginOccupied']])
                else:
                    tempAgNode['卖'] = int(node[positions['Lots']])
                    tempAgNode['卖成交价'] = Decimal(node[positions['AvgOpenPrice']])
                    tempAgNode['卖保证金占用'] = Decimal(node[positions['MarginOccupied']])

                #tempAgNode['手续费'] = Decimal(node['手续费'])
                tempAgNode['合约'] = node[positions['Instrument']]
                #tempAgNode['投/保'] = node['投/保']
                tempAgNode['持仓盯市盈亏'] = Decimal(node[positions['MTMP/L']])
                setDet[node[positions['Instrument']]] = tempAgNode
            else:
                tempAgNode = setDet[node[positions['Instrument']]]
                #print(tempSDNode)
                if '买' in node[positions['B/S']]:
                    oldBuyAvg = tempAgNode['买成交价']
                    oldBuySum = tempAgNode['买']
                    nodeBuyAvg = Decimal(node[positions['AvgOpenPrice']])
                    nodeBuySum = int(node[positions['Lots']])
                    newBuyAvg = oldBuyAvg * oldBuySum + nodeBuyAvg * nodeBuySum
                    newBuyAvg = newBuyAvg / (oldBuySum + nodeBuySum)
                    tempAgNode['买成交价'] = newBuyAvg
                    tempAgNode['买'] += int(node[positions['Lots']])
                    tempAgNode['买保证金占用'] += Decimal(node[positions['MarginOccupied']])
                else:
                    oldSellAvg = tempAgNode['卖成交价']
                    oldSellSum = tempAgNode['卖']
                    nodeSellAvg = Decimal(node[positions['AvgOpenPrice']])
                    nodeSellSum = int(node[positions['Lots']])
                    newSellAvg = oldSellAvg * oldSellSum + nodeSellAvg * nodeSellSum
                    newSellAvg = newSellAvg / (oldSellSum + nodeSellSum)
                    tempAgNode['卖保证金占用'] += Decimal(node[positions['MarginOccupied']])
                    tempAgNode['卖成交价'] = newSellAvg
                    tempAgNode['卖'] += int(node[positions['Lots']])
                tempAgNode['持仓盯市盈亏'] += Decimal(node[positions['MTMP/L']])
    #aggregate all positons
    for futureID in setDet:
        tempAgNode = setDet[futureID]
        if tempAgNode['买保证金占用'] >= tempAgNode['卖保证金占用']:
            tempAgNode['单边最大方向'] = '买'
        else:
            tempAgNode['单边最大方向'] = '卖'
    return setDet

def main():

    path = './txt'
    subAccPath = './subacc';
    presentCTPBill = './presentCTPBill'
    #subAccPath = presentCTPBill

    textContainer = readBill_All(subAccPath)

    #aggregateFutures tempAgg();
    posAeg = aggregate(textContainer)

    for text in textContainer:
        tempKN = kingNew(text, posAeg)
        tempKN.clear();
        del tempKN



    print("\n程序运行正常结束！")
    #raw_input()
    #test = float(input())


    os.system("pause")
    return

if __name__=="__main__":
    main()
