# -*- coding: utf-8 -*-
import os
import re
# import datetime
#
# from decimal import *
# from KingNewSchema import GSaccShema
# import dbf
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt

import logging
import logging.handlers
import logging.config



Gdebug = False

       # 品种       |      合约      |    买持     |    买均价   |     卖持     |    卖均价    |  昨结算  |  今结算  |持仓盯市盈亏|  保证金占用   |  投/保     |   多头期权市值   |   空头期权市值    |
       # |成交日期| 交易所 |       品种       |      合约      |买/卖|   投/保    |  成交价  | 手数 |   成交额   |       开平       |  手续费  |  平仓盈亏  |     权利金收支      |  成交序号  |
GPaDec = ["买持", "买均价", "卖持", "卖均价", "昨结算", "今结算", "持仓盯市盈亏", "保证金占用", "多头期权市值", "空头期权市值",
          "成交价", "手数", "成交额", "手续费", "平仓盈亏", "权利金收支"
          ]
#keyWords = ['结算单', '资金状况', '持仓明细', '持仓汇总', '成交明细', '平仓明细', '出入金明细', '中信期货']
pBillKeys = {'交易结算单(盯市)', '资金状况', '成交记录', '平仓明细', '持仓明细', '持仓汇总'}
pBillDicts = {"SettlementStatement" : "交易结算单(盯市)", "AccountSummary" : "资金状况", "TransactionRecord" : "成交记录", "PositionClosed" : "平仓明细", "PositionsDetail" : "持仓明细", "Positions" : "持仓汇总"}

GParentSettlement ={'clientID': '客户号', 'Date':'日期'}

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
    def writeDeliveryDbf(self, path):

        return
    def writeDepositDbf(self, path):
        return
    def writePosDbf(self, path):
        return
    def writeTransDbf(self, path):

        return
    def writeAccDbf(self, path):

        # global  GSaccShema
        # # GSaccShema = {"PreBalance":'上次结算资金', 'DeliveryFee':'交割手续费', 'DepositWithdrawal': '出入金',
        # #     'Balancecf':'期末结存', 'RealizedPL':'平仓盈亏', 'MarginOccupied':'保证金占用', 'MTMPL':'持仓盈亏',
        # #     'Fund Avail':'可用资金', 'Fee':'手续费', 'RiskDegree':'风险度'}
        # temphead = {}
        # temphead['结算会员号'] = str(self.__account)
        # table = dbf.Table(path)
        # table.open()
        # copyTable = table.new('./output/'+ self.__account + '_' + self.__mydate + '_capital.dbf')
        # copyTable.open()
        #
        #
        # rows = []
        # rows.append((temphead['结算会员号'], '上一交易日实有货币资金余额', str(self.__Balance_bf)))
        # rows.append((temphead['结算会员号'],'加：当日收入资金', str(self.__Deposit)))
        # rows.append((temphead['结算会员号'], '当日盈亏', str(self.__MTM)))
        # rows.append((temphead['结算会员号'],'减：当日付出资金', str(self.__Payment)))
        # rows.append((temphead['结算会员号'], '手续费', str(self.__Commission)))
        # rows.append((temphead['结算会员号'], '其中：交易手续费', str(self.__Commission)))
        # rows.append((temphead['结算会员号'], '结算手续费', '0.00'))
        # rows.append((temphead['结算会员号'],'交割手续费', '0.00'))
        # rows.append((temphead['结算会员号'], '移仓手续费', '0.00'))
        # rows.append((temphead['结算会员号'], '当日实有货币资金余额', str(self.__Balance_cf)))
        # rows.append((temphead['结算会员号'],'其中：交易保证金', str(self.__Margin_Occupied)))
        # rows.append((temphead['结算会员号'],  '结算准备金', str(self.__Fund_Avail)))
        # rows.append((temphead['结算会员号'],  '减：交易保证金', str(self.__Margin_Occupied)))
        # rows.append((temphead['结算会员号'],  '当日结算准备金余额', str(self.__Fund_Avail)))
        # rows.append((temphead['结算会员号'],  '加：申报划入金额', '0.00'))
        # rows.append((temphead['结算会员号'],  '减：申报划出金额', '0.00'))
        # rows.append((temphead['结算会员号'],  '下一交易日开仓准备金', str(self.__Fund_Avail)))
        # rows.append((temphead['结算会员号'], '其它', '-' ))
        # rows.append((temphead['结算会员号'], '应收手续费', str(self.__Commission )))
        # rows.append( (temphead['结算会员号'], '实有货币资金变动', str(float(self.__MTM) + float(self.__Realized )) ))
        # rows.append((temphead['结算会员号'], '其中：交易保证金变动', '0.00' ))
        # rows.append((temphead['结算会员号'], '结算准备金变动', '0.00'))
        #
        # s =  r'上一交易日实有货币资金余额'
        # #s.decode('UTF-8')
        # #table.append( ('13887', '上一交易日实有货币资金余额', '10000.00') )
        # for datum in rows:
        #     #table.append(datum)
        #     copyTable.append(datum)
        #
        # copyTable.close()
        # table.close()
        return

    def writeDbf(self):


        return
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
        for line in txt:
            self.settlementTxt.append(line)
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

            singleRow = txtlist[index]
            vals = self.splitToData(singleRow)
            if not vals:
                break
            # vals = singleRow.split('|')
            # vals = vals[1:-1]
            # cleanVals = []
            # for eachVal in vals:
            #     cleanVals.append(eachVal.strip())
            # vals = cleanVals
                # print(eachVal.strip())
            # collectVal = re.compile(u'\d*[\u4e00-\u9fa5]+\d+[\u4e00-\u9fa5]*|[A-Za-z]{1,2}\d{3,4}|[-+]?\d+\.?\d+|[\u4e00-\u9fa5]+|\d');
            # vals = collectVal.findall(txtlist[index])
            # vals = cleanVals
            if '共' in vals[0]:
                break
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
        #(list)
        df = pd.DataFrame(list, columns = keys)
        # print(df)
        return df
    def splitToData(self, row):
        res = []
        vals = row.split('|')
        vals = vals[1:-1]
        cleanVals = []
        for eachVal in vals:
            cleanVals.append(eachVal.strip())
        # vals = cleanVals
        if '共' in vals[0]:
            return res
        res = cleanVals
        return res
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
            singleRow = txtlist[index]
            vals = self.splitToData(singleRow)
            if not vals:
                break
            # singleRow = txtlist[index]
            # vals = singleRow.split('|')
            # vals = vals[1:-1]
            # cleanVals = []
            # for eachVal in vals:
            #     cleanVals.append(eachVal.strip())
            # vals = cleanVals
            # collectVal = re.compile(u'[\u4e00-\u9fa5]+\d+[\u4e00-\u9fa5]*|[A-Za-z]{1,2}\d{3,4}|[-+]?\d+\.?\d+|[\u4e00-\u9fa5]+|\d');
            # vals = collectVal.findall(txtlist[index])
            if '共' in vals[0]:
                break
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
        #print(df)
        return df


    def setAccNdate(self, txt = []):
        #GParentSettlement ={'clientID': '客户号', 'Date':'日期'}
        global GParentSettlement
        #global GParentSettlement
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

        if GParentSettlement['clientID'] in NameToValue:
            self.__accNum = NameToValue[GParentSettlement['clientID']]
        elif  '客户号' in NameToValue:
            self.__accNum = NameToValue[GParentSettlement['clientID']]
        else:
            print('账户没有正确解析')
            self.__accNum = 'NULL'
        self.__date = NameToValue[GParentSettlement['Date']]
        #结算会员:13887    结算会员名称:中信期货(0018)   结算日期:20161213
        #self.__strHeader = '结算会员: ' + self.__accNum[0:-2] + '       结算会员名称:中信期货(0018)' + '      结算日期:' + self.__date
        self.__strHeader = '结算会员: ' + self.__accNum + '       结算会员名称:中信期货(0018)' + '      结算日期:' + self.__date
        return
    def toNum(self, pdata):
        global GPaDec
        print(pdata.dtypes)
        pCols = pdata.columns
        for eachCol in pCols:
            if eachCol in GPaDec:
                try:
                    pdata[eachCol] = pdata[eachCol].astype(float)
                except Exception as e:
                    print(pdata[eachCol])
                    print(pdata[eachCol].dtype)
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


        if self.settlementTxt:
            self.setAccNdate(self.settlementTxt)

        if self.positionsTxt:
            self.positionList = self.washPosition(self.positionsTxt)
            self.toNum(self.positionList)
        if self.transactionTxt:
            self.transList = self.washTrantransaction(self.transactionTxt)
            self.toNum(self.transList)
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

    def getPBillKeys(self):
        keys = []
        keys = self.__BillDict.keys()
        return keys
    def getPBill(self, key):

        pBill = self.__BillDict[key]
        return pBill
    def getBills(self):
        self.__BillDict = {}
        for acc in self.textList:
            temp_txt = self.textList[acc]
            pBill = ParentBill(temp_txt)
            self.__BillDict[acc] = pBill

        return
    def getAcc(self, file_name):
        ans = ""
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
