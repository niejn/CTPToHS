# -*- coding: utf-8 -*-
import os
import re
import datetime

from decimal import *
from prettytable import *
import dbf
import pandas as pd
from KingNewSchema import *

import logging
import logging.handlers
import logging.config
from billRead import Bill

#----------------------------------------------------------------------
logging.config.fileConfig('logging.conf')

child_logger = logging.getLogger('bill')
#logger = logging.getLogger('billRead')
child_logger.info('test child bill logger')


# 手数 |    开仓价   |    结算价   |   持仓盈亏  |    保证金
#  手数 |    开仓价   |    结算价   |   持仓盈亏  |    保证金
# 手数 |       开仓均价  |        结算价   |     持仓盯市盈亏|    保证金占用
# 成交价|  手数 |  开平 |      手续费   |      成交编号
# 开仓价|       平仓价|  手数 |  开平 |   平仓盈亏  | 投/保|     成交编号
GChildDec = ["手数", "开仓价", "结算价", "持仓盈亏", "保证金", "开仓均价", "持仓盯市盈亏", "保证金占用",
             "成交价", "手续费", "平仓价", "平仓盈亏"]
# keyWords = ['结算单', '资金状况', '持仓明细', '持仓汇总', '成交明细', '平仓明细', '出入金明细', '中信期货']
#KN_Keys = ['结算单', '资金状况', '持仓明细', '持仓汇总', '成交明细', '平仓明细', '出入金明细', '中信期货']
    # operator = {'结算单':setSettlementTxt, '资金状况':setAccountTxt, '持仓明细':setPositionsDetailTxt,
    #             '持仓汇总':setPositionsTxt, '成交明细':setTransactionTxt, '平仓明细':setRealizeTxt, '交割明细':setDeliveryTxt,
    #             '中信期货':setCompTxt, '出入金明细':setDepositNWithdraw}
KN_Keys = ['结算单', '资金状况', '持仓明细', '持仓汇总', '成交明细', '平仓明细', '出入金明细', '中信期货', '交割明细']
KN_Dicts = {"SettlementStatement" : "结算单", "AccountSummary" : "资金状况", "TransactionRecord" : "成交明细",
            "PositionClosed" : "平仓明细", "PositionsDetail" : "持仓明细", "Positions" : "持仓汇总",
            "Delivery" : "交割明细", "Company" : '中信期货', "DepositNWithdraw" : '出入金明细'}
GSsettlement ={'clientID': '账户', 'Date':'日期'}


class childBill(Bill):

    def setSettlementTxt(self, txt = []):
        for line in txt:
            self.settlementTxt.append(line)
        return
    def setAccountTxt(self, txt = []):
        self.accountTxt.extend(txt)
        return
    def setPositionsDetailTxt(self, txt = []):
        self.positionsDetailTxt.extend(txt)
        return
    def setPositionsTxt(self, txt = []):
        self.positionsTxt.extend(txt)
        return
    def setTransactionTxt(self, txt = []):
        self.transactionTxt.extend(txt)
        return

    def setRealizeTxt(self, txt = []):
        self.realizeTxt.extend(txt)
        return
    def setDeliveryTxt(self, txt = []):
        self.deliveryTxt.extend(txt)
        return
    def setCompTxt(self, txt = []):
        return
    def setDepositNWithdraw(self, txt = []):
        self.depositTxt.extend(txt)
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
    def setAccNdate(self, txt = []):
        #GSsettlement ={'clientID': '账户', 'Date':'日期'}
        global GSsettlement
        NameToValue = {}
        for line in txt[1:]:

            str =line.split()
            phanzi=re.compile(u'[\u4e00-\u9fa5]+');

            res = phanzi.findall(line)
            nums = re.findall(r'([a-zA-Z]*\d+)', line)



            resLen = res.__len__()
            numsLen = nums.__len__()
            len = resLen if resLen < numsLen else numsLen

            for index in range(len):
                NameToValue[res[index]] = nums[index]

        if GSsettlement['clientID'] in NameToValue:
            self.__accNum = NameToValue[GSsettlement['clientID']]
        elif  '客户号' in NameToValue:
            self.__accNum = NameToValue[GSsettlement['clientID']]
        else:
            print('账户没有正确解析')
            self.__accNum = 'NULL'
        self.__date = NameToValue[GSsettlement['Date']]
        #结算会员:13887    结算会员名称:中信期货(0018)   结算日期:20161213
        #self.__strHeader = '结算会员: ' + self.__accNum[0:-2] + '       结算会员名称:中信期货(0018)' + '      结算日期:' + self.__date
        self.__strHeader = '结算会员: ' + self.__accNum + '       结算会员名称:中信期货(0018)' + '      结算日期:' + self.__date
        return
    def washPosition(self, txtlist = []):
        #print(txtlist)
        index = 0
        #filter the header and nonsense lines
        while("|" not in txtlist[index]):
            index += 1
        schema_txt = txtlist[index]
        phanzi = re.compile(u'[\u4e00-\u9fa5]+\/?[\u4e00-\u9fa5]+');
        keys = phanzi.findall(schema_txt)
        keySize = len(keys)

        # there is no need for fiter the english key
        # #filter the english key
        # index += 2
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
                child_logger.error("in washPosition of ParentBill valSize not equal to keySize")
                child_logger.error(vals)
            else:
                # temp = {}
                # for index in range(len(keys)):
                #     temp[keys[index]] = vals[index]

                list.append(vals)
            index += 1

            #vals = txtlist[index].split('|')
        #print(list)
        df = pd.DataFrame(list, columns = keys)
        # print(df)
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
                child_logger.error("in washPosition of ParentBill valSize not equal to keySize")
                child_logger.error(vals)
            else:
                # temp = {}
                # for index in range(len(keys)):
                #     temp[keys[index]] = vals[index]

                list.append(vals)
            index += 1

            #vals = txtlist[index].split('|')
        #print(list)
        df = pd.DataFrame(list, columns = keys)
        # print(df)
        return df

        return
    def washAccount(self, txt = []):

        NameToValue = {}
        for line in txt[1:]:

            str = ' '.join(line.split())
            phanzi=re.compile(u'[\u4e00-\u9fa5]+[\s]?[\u4e00-\u9fa5]+[\s]?[\u4e00-\u9fa5]+');

            res = phanzi.findall(str)
            nums = re.findall(r'([-+]?\d+\.\d+)', str)

            resLen = res.__len__()
            numsLen = nums.__len__()
            len = resLen if resLen < numsLen else numsLen

            for index in range(len):
                NameToValue[res[index]] = nums[index]
        return NameToValue
    def toNum(self, pdata):
        global GChildDec
        print(pdata.dtypes)
        pCols = pdata.columns
        for eachCol in pCols:
            if eachCol in GChildDec:
                pdata[eachCol] = pdata[eachCol].astype(float)
                # pdata[eachCol] = pdata[eachCol].astype(Decimal)
                #print(pdata[eachCol])
        #print(pdata.dtypes)

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
        global KN_Keys
        global KN_Dicts
        self.keyWords = KN_Keys

        self.operator = {KN_Dicts['SettlementStatement']: self.setSettlementTxt, KN_Dicts['AccountSummary']: self.setAccountTxt, KN_Dicts['PositionsDetail']: self.setPositionsDetailTxt,
                        KN_Dicts['Positions']: self.setPositionsTxt, KN_Dicts['TransactionRecord']: self.setTransactionTxt, KN_Dicts['PositionClosed']: self.setRealizeTxt,
                        KN_Dicts['Delivery']: self.setDeliveryTxt, KN_Dicts['Company']: self.setCompTxt, KN_Dicts['DepositNWithdraw']: self.setDepositNWithdraw}



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

        if self.settlementTxt:
            self.setAccNdate(self.settlementTxt)
        if self.accountTxt:
            self.accountDict = self.washAccount(self.accountTxt)
        if self.positionsDetailTxt:
            self.positionsDetailList = self.washPosition(self.positionsDetailTxt)
            self.toNum(self.positionsDetailList)
        if self.deliveryTxt:
            self.deliveryList = self.washPosition(self.deliveryTxt)
            self.toNum(self.deliveryList)
        if self.depositTxt:
            self.depositList = self.washPosition(self.depositTxt)
            self.toNum(self.depositList)
        if self.positionsTxt:
            self.positionList = self.washPosition(self.positionsTxt)
            self.toNum(self.positionList)
        if self.transactionTxt:
            self.transList = self.washPosition(self.transactionTxt)
            self.toNum(self.transList)





        return


def readSingleBill(file):


    if not os.path.isfile(file):
        return
    with open(file, 'rb') as srcFile:
        # textlist = srcFile.readlines()
        content = srcFile.read().decode('utf-8')

        textlist = content.split('\n')

    return textlist
def main():

    path = './txt'
    subAccPath = './subacc/120200889072017-02-16.txt';
    txt = readSingleBill(subAccPath)
    cbill = childBill(txt)
    # parentAccPath = "./parentAcc"
    # presentCTPBill = './presentCTPBill'





    print("\n程序运行正常结束！")


    os.system("pause")
    return

if __name__=="__main__":
    main()