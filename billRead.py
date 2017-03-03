# -*- coding: utf-8 -*-
import os
import re
import datetime

from decimal import *
from prettytable import *
import dbf
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt

import logging
import logging.handlers
import logging.config


Gdebug = False

#keyWords = ['结算单', '资金状况', '持仓明细', '持仓汇总', '成交明细', '平仓明细', '出入金明细', '中信期货']
pBillKeys = {'交易结算单(盯市)', '资金状况', '成交记录', '平仓明细', '持仓明细', '持仓汇总'}
pBillDicts = {"SettlementStatement" : "交易结算单(盯市)", "AccountSummary" : "资金状况", "TransactionRecord" : "成交记录", "PositionClosed" : "平仓明细", "PositionsDetail" : "持仓明细", "Positions" : "持仓汇总"}

#----------------------------------------------------------------------
logging.config.fileConfig('logging.conf')
root_logger = logging.getLogger('root')
root_logger.info('root logger')
logger = logging.getLogger('main')
#logger = logging.getLogger('billRead')
logger.info('test main logger')
#logging.ERROR
bill_logger = logging.getLogger('bill')
bill_logger.error("This is warning message")
    # except:
    #     logger.exception("Exception Logged")
# def initialLogger():
#     logging.basicConfig(level=logging.DEBUG,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename='myapp.log',
#                 filemode='w')
#
#     #################################################################################################
#     #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
#     console = logging.StreamHandler()
#     console.setLevel(logging.INFO)
#     formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#     console.setFormatter(formatter)
#     logging.getLogger('').addHandler(console)
#     logging.debug('This is debug message')
#     logging.info('This is info message')
#     logging.warning('This is warning message')
#     logging.error("This is warning message")
#     return


class Bill:

    def __init__(self, textList = []):
        self.settlementTxt = []
        self.accountTxt = []
        self.depositTxt = []
        self.transactionTxt = []
        self.realizeTxt = []
        self.deliveryTxt = []
        self.positionsDetailTxt = []
        self.positionsTxt = []
        name = ''
        block = []
        for line in textList:
            #remove all invisiable tag like \r \n space and so on
            if (not line) or (not line.strip('\n')) or (self.isGarbageLine(line)) or (not line.strip('\r')):
                    continue
            else:
                    if len(line) > 0 and line:
                        block.append(line.strip())

        self.cleanRawTxt(block)

        return
    def isGarbageLine(self, txt):
        ans = False
        phanzi=re.compile(u'[\u4e00-\u9fa5]+');

        #res = phanzi.findall(line)
        if '---' in txt:
            res = phanzi.findall(txt)
            if res:
                #txt = res[0]
                ans = False

            else:
                ans = True
        else:
            ans = False

        return ans

    def setSettlementTxt(self, txt = []):
        # for line in txt:
        #     self.settlementTxt.append(line)
        return
    def setAccountTxt(self, txt = []):
        #self.accountTxt.extend(txt)
        return
    def setPositionsDetailTxt(self, txt = []):
        #self.positionsDetailTxt.extend(txt)
        return
    def setPositionsTxt(self, txt = []):
        self.positionsTxt.extend(txt)
        return
    def setTransactionTxt(self, txt = []):
        #self.transactionTxt.extend(txt)
        return

    def setRealizeTxt(self, txt = []):
        #self.realizeTxt.extend(txt)
        return
    def setDeliveryTxt(self, txt = []):
        #self.deliveryTxt.extend(txt)
        return
    def setCompTxt(self, txt = []):
        return
    def setDepositNWithdraw(self, txt = []):
        #self.depositTxt.extend(txt)
        return
    # operator = {'结算单':setSettlementTxt, '资金状况':setAccountTxt, '持仓明细':setPositionsDetailTxt,
    #             '持仓汇总':setPositionsTxt, '成交明细':setTransactionTxt, '平仓明细':setRealizeTxt, '交割明细':setDeliveryTxt,
    #             '中信期货':setCompTxt, '出入金明细':setDepositNWithdraw}

    def cleanRawTxt(self,txt):
        global pBillDicts

        self.keyWords = pBillDicts
        #pBillDicts = {"SettlementStatement" : "交易结算单(盯市)", "AccountSummary" : "资金状况", "TransactionRecord" : "成交记录", "PositionClosed" : "平仓明细", "PositionsDetail" : "持仓明细", "Positions" : "持仓汇总"}
        self.operator = {pBillDicts['SettlementStatement']: self.setSettlementTxt, pBillDicts['AccountSummary']: self.setAccountTxt, pBillDicts['PositionsDetail']: self.setPositionsDetailTxt,
                pBillDicts['Positions']: self.setPositionsTxt, pBillDicts['TransactionRecord']: self.setTransactionTxt, pBillDicts['PositionClosed']: self.setRealizeTxt}


        cleanTxt = []
        txtcup = []
        tempkey = ''
        newBlock = False
        #self.cleanDBFTables(self.__myDBFPath)
        GenTxt = False
        for line in txt:
            if line:
                for key in self.keyWords:
                    if key in line:
                        if txtcup:
                            if tempkey in self.operator:
                                self.operator.get(tempkey)(txtcup)
                            txtcup.clear()
                        tempkey = key
                        newBlock = True
                        break
                if len(line) > 0:
                    txtcup.append(line)


        if txtcup:
            self.operator.get(tempkey)(self, txtcup)
            txtcup.clear()
        # if self.settlementTxt:
        #     self.setAccNdate(self.settlementTxt)
        # if self.accountTxt:
        #     self.__myAcc.set(self.accountTxt)
            #self.__myAcc.setAccNdate(self.__accNum, self.__date)
        positionList = {}
        if self.positionsTxt:
            positionList = self.__myPositions.set(self.positionsTxt)


        return positionList
    def read(self):

        return
    def readAll(self, path):
        files = os.listdir(path)
        textContainer = []
        for file in files:
            file = path + '/' + file
            if not os.path.isfile(file):
                continue
            if file.endswith('txt'):
                with open(file, 'rb') as srcFile:
                    #content = fp.read().decode('utf-8')
                    content = srcFile.read().decode('gbk')
                    # for oneline in content:
                    #     oneline.decode('utf-8')
                    #content = content.strip('\r')
                    text = content.split('\n')


                    #text = srcFile.readlines()
                textContainer.append(text)
                srcFile.close()

        return textContainer







class ParentBill(Bill):

    def setSettlementTxt(self, txt = []):
        # for line in txt:
        #     self.settlementTxt.append(line)
        return
    def setAccountTxt(self, txt = []):
        #self.accountTxt.extend(txt)
        return
    def setPositionsDetailTxt(self, txt = []):
        #self.positionsDetailTxt.extend(txt)
        return
    def setPositionsTxt(self, txt = []):
        self.positionsTxt.extend(txt)
        return
    def setTransactionTxt(self, txt = []):
        self.transactionTxt.extend(txt)
        return

    def setRealizeTxt(self, txt = []):
        #self.realizeTxt.extend(txt)
        return
    def setDeliveryTxt(self, txt = []):
        #self.deliveryTxt.extend(txt)
        return
    def setCompTxt(self, txt = []):
        return
    def setDepositNWithdraw(self, txt = []):
        #self.depositTxt.extend(txt)
        return
    def isGarbageLine(self, txt):
        ans = False
        phanzi=re.compile(u'[\u4e00-\u9fa5]+');
        if len(txt) > 0:

            #res = phanzi.findall(line)
            if '---' in txt:
                res = phanzi.findall(txt)
                if res:
                    #txt = res[0]
                    ans = False

                else:
                    ans = True
            else:
                ans = False
        else:
            ans = True

        return ans
    def washPosition(self, txtlist = []):
        print(txtlist)
        index = 0
        #filter the header and nonsense lines
        while("|" not in txtlist[index]):
            index += 1
        schema_txt = txtlist[index]
        phanzi = re.compile(u'[\u4e00-\u9fa5]+\/?[\u4e00-\u9fa5]+');
        keys = phanzi.findall(schema_txt)
        keySize = len(keys)
        #filter the english key
        index += 2
        #filter the nonsense line
        list = []
        while(index < len(txtlist)):

            if "|" not in txtlist[index]:
                break;

            # testVal = re.compile(u'[^\|]*');
            # vals = testVal.findall(txtlist[index])
            collectVal = re.compile(u'[\u4e00-\u9fa5]+\d+[\u4e00-\u9fa5]*|[A-Za-z]{1,2}\d{3,4}|[-+]?\d+\.?\d+|[\u4e00-\u9fa5]+|\d');
            vals = collectVal.findall(txtlist[index])
            if len(vals) != keySize:
                logger.error("in washPosition of ParentBill valSize not equal to keySize")
                logger.error(vals)
            else:
                # temp = {}
                # for index in range(len(keys)):
                #     temp[keys[index]] = vals[index]

                list.append(vals)
            index += 1

            #vals = txtlist[index].split('|')
        print(list)
        df = pd.DataFrame(list, columns = keys)
        print(df)
        return df

    def washTrantransaction(self,txtlist = []):
        #print(txtlist)
        index = 0
        #filter the header and nonsense lines
        while("|" not in txtlist[index]):
            index += 1
        schema_txt = txtlist[index]
        phanzi = re.compile(u'[\u4e00-\u9fa5]+\/?[\u4e00-\u9fa5]+');
        keys = phanzi.findall(schema_txt)
        keySize = len(keys)
        #filter the english key
        index += 2
        #filter the nonsense line
        list = []
        while(index < len(txtlist)):

            if "|" not in txtlist[index]:
                break;

            # testVal = re.compile(u'[^\|]*');
            # vals = testVal.findall(txtlist[index])
            collectVal = re.compile(u'[\u4e00-\u9fa5]+\d+[\u4e00-\u9fa5]*|[A-Za-z]{1,2}\d{3,4}|[-+]?\d+\.?\d+|[\u4e00-\u9fa5]+|\d');
            vals = collectVal.findall(txtlist[index])
            if len(vals) != keySize:
                logger.error("in washPosition of ParentBill valSize not equal to keySize")
                logger.error(vals)
            else:
                # temp = {}
                # for index in range(len(keys)):
                #     temp[keys[index]] = vals[index]

                list.append(vals)
            index += 1

            #vals = txtlist[index].split('|')
        #print(list)
        df = pd.DataFrame(list, columns = keys)
        print(df)
        return df

        return
    def cleanRawTxt(self,txt):
        self.settlementTxt = []
        self.accountTxt = []
        self.depositTxt = []
        self.transactionTxt = []
        self.realizeTxt = []
        self.deliveryTxt = []
        self.positionsDetailTxt = []
        self.positionsTxt = []
        global pBillDicts
        global pBillKeys
        self.keyWords = pBillKeys
        #pBillDicts = {"SettlementStatement" : "交易结算单(盯市)", "AccountSummary" : "资金状况", "TransactionRecord" : "成交记录", "PositionClosed" : "平仓明细", "PositionsDetail" : "持仓明细", "Positions" : "持仓汇总"}
        self.operator = {pBillDicts['SettlementStatement']: self.setSettlementTxt, pBillDicts['AccountSummary']: self.setAccountTxt, pBillDicts['PositionsDetail']: self.setPositionsDetailTxt,
                pBillDicts['Positions']: self.setPositionsTxt, pBillDicts['TransactionRecord']: self.setTransactionTxt, pBillDicts['PositionClosed']: self.setRealizeTxt}


        cleanTxt = []
        txtcup = []
        tempkey = ''
        newBlock = False
        #self.cleanDBFTables(self.__myDBFPath)
        GenTxt = False
        for line in txt:
            if line:
                for key in self.keyWords:
                    if key in line:
                        if txtcup:
                            if tempkey in self.operator:
                                self.operator.get(tempkey)(txtcup)
                            txtcup.clear()
                        tempkey = key
                        newBlock = True
                        break
                if len(line) > 0:
                    txtcup.append(line)


        if txtcup:
            self.operator.get(tempkey)(txtcup)
            txtcup.clear()


        if self.positionsTxt:
            self.positionList = self.washPosition(self.positionsTxt)
        if self.transactionTxt:
            # for line in self.transactionTxt:
            #     print(line)
            self.transList = self.washTrantransaction(self.transactionTxt)

        return






class BillList:
    def __init__(self, path):
        self.textList = self.readAll(path)
        self.getBills()
        #self.txtGroup =
        return
    def getBills(self):

        return
    def getAcc(self, file_name):


        return

    def readAll(self, path):
        files = os.listdir(path)
        textContainer = []
        txtDict = {}
        for file in files:
            txt_key = file
            file = path + '/' + file
            if not os.path.isfile(file):
                continue
            if file.endswith('txt'):
                with open(file, 'rb') as srcFile:
                    #content = fp.read().decode('utf-8')
                    content = srcFile.read().decode('gbk')
                    # for oneline in content:
                    #     oneline.decode('utf-8')
                    #content = content.strip('\r')
                    text = content.split('\n')



                textContainer.append(text)
                # srcFile.close()
            txtDict[txt_key] = textContainer

        return txtDict
class ParentBillList(BillList):
    def getBills(self):
        self.__BillDict = {}
        for acc in self.textList:
            temp_txt = self.textList[acc]
            pBill = ParentBill(temp_txt)
            self.__BillDict[acc] = pBill

        return
    def getAcc(self, file_name):
        ans = NONE
        #20170216_120200888_交易结算单.txt
        #phanzi = re.compile(u'[\u4e00-\u9fa5]+');
        phanzi = re.compile(u'[0-9]+');
        keys = phanzi.findall(file_name)
        #keySize = keys.__len__()
        ans = keys[-1]
        return ans

    def readAll(self, path):
        files = os.listdir(path)
        textContainer = []
        txtDict = {}
        for file in files:
            txt_key = self.getAcc(file)
            file = path + '/' + file
            if not os.path.isfile(file):
                continue
            if file.endswith('txt'):
                with open(file, 'rb') as srcFile:
                    #content = fp.read().decode('utf-8')
                    content = srcFile.read().decode('gbk')
                    # for oneline in content:
                    #     oneline.decode('utf-8')
                    #content = content.strip('\r')
                    text = content.split('\n')



                #textContainer.append(text)
                # srcFile.close()
            txtDict[txt_key] = text
            text = []

        return txtDict

def main():

    path = './txt'
    subAccPath = './subacc';
    parentAccPath = "./parentAcc"
    presentCTPBill = './presentCTPBill'
    #subAccPath = presentCTPBill

    #textContainer = Bill.readBill_All(parentAccPath)
    pbills = ParentBillList(parentAccPath)




    print("\n程序运行正常结束！")


    os.system("pause")
    return

if __name__=="__main__":
    main()
