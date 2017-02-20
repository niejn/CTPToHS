# -*- coding: utf-8 -*-
__author__ = 'lenovo'
import os
import re
import datetime

from decimal import *
from prettytable import *
import dbf

Gdebug = False

class positions:#持仓汇总
    #对应dbf文件中的settlementdetail
    __name = '持仓汇总'
    __myList = []
    IDToMultiplier = {}
    __account = ''
    __mydate = ''
    __Clientids = []
    __Userid = []
    __Partid = []
    __accdata = {}
    __customer_Clientid = {}
    __customer_Userid = {}
    __broker_Partid = {}
    __FutToExchange = {}
    __FutToPartid = {}
    __FutToClientid = {}
    def clear(self):

        return
    def readConfig(self):
        config = open('./futuresConfig.txt', 'r')
        textlist = config.readlines()
        futureID = re.compile(u'[a-zA-Z]+');
        multiplier = re.compile(u'\d+');
        for item in textlist:
            id = futureID.findall(item)
            mul = multiplier.findall(item)
            self.IDToMultiplier[id[0].upper()] = int(mul[0])

        config.close()

        accConfig = open('./acountConfig.txt', 'r')
        textlist = accConfig.readlines()
        ID = re.compile(u'[a-zA-Z_a-zA-Z]+');
        multiplier = re.compile(u'\d+');
        # customer_Clientid = {}
        # customer_Userid = {}
        # broker_Partid = {}
        operater = {"customer_Clientid": self.__customer_Clientid, "customer_Userid": self.__customer_Userid, "broker_Partid": self.__broker_Partid}
        #accdata = {}
        temp = {}
        key = ''
        for item in textlist:

            if "#" in item:
                id = ID.findall(item)
                temp = operater[id[0]]
            else:

                id = ID.findall(item)
                mul = multiplier.findall(item)
                temp[id[0]] = mul[0]
        accConfig.close()

        futConfig = open('./config.ini', 'r')
        textlist = futConfig.readlines()
        getWord = re.compile(u'[a-zA-Z]+');
        multiplier = re.compile(u'\d+');

        tExchange = ''
        tFuture = ''
        for item in textlist:

            if "#" in item:
                tWords = getWord.findall(item)
                tExchange = tWords[0]
            else:
                tWords = getWord.findall(item)
                tFuture = tWords[0]
                self.__FutToExchange[tFuture] = tExchange
                self.__FutToClientid[tFuture] = self.__customer_Clientid[tExchange]
                self.__FutToPartid[tFuture] = self.__broker_Partid[tExchange]



        return
    def __init__(self):
        self.__name = '持仓汇总'
        self.__myList = []
        self.IDToMultiplier = {}
        self.__account = ''
        self.__mydate = ''
        self.__Clientids = []
        self.__Userid = []
        self.__Partid = []
        self.__accdata = {}
        self.__customer_Clientid = {}
        self.__customer_Userid = {}
        self.__broker_Partid = {}
        self.__FutToExchange = {}
        self.__FutToPartid = {}
        self.__FutToClientid = {}
        self.__myList.clear()

        self.IDToMultiplier.clear()

        self.__Clientids.clear()
        self.__Userid.clear()
        self.__Partid.clear()
        self.__accdata.clear()
        self.__customer_Clientid.clear()
        self.__customer_Userid.clear()
        self.__broker_Partid.clear()
        self.__FutToExchange.clear()
        self.__FutToPartid.clear()
        self.__FutToClientid.clear()


        __myName = '持仓汇总'
        if Gdebug:
            print(__myName)
        self.readConfig()

        return
    def getPostions(self):

        return self.__myList
    def set(self, txt = []):
        if not txt:
            if Gdebug:
                print("positions txt is empty！")
            return
        list = []
        phanzi = re.compile(u'[\u4e00-\u9fa5]+\/?[\u4e00-\u9fa5]+');
        keys = phanzi.findall(txt[1])
        keySize = keys.__len__()
        temp = {}
        for line in txt[2:]:



            collectVal = re.compile(u'[A-Za-z]{1,2}\d{3,4}|[-+]?\d+\.?\d+|[\u4e00-\u9fa5]+|\d');
            val = collectVal.findall(line)
            valSize = val.__len__()
            if Gdebug:
                print(val)
            temp = {}

            if keySize != valSize:
                if Gdebug:
                    print("keySize: " + str(keySize) + " valSize: " + str(valSize))
            else:
                for index in range(len(keys)):
                    temp[keys[index]] = val[index]
                self.__myList.append(temp)
                list.append(temp)
        if Gdebug:
            print(self.__myList)
            print(list)
        return list
    def setAccNdate(self, acc, date):
        self.__account = acc
        self.__mydate = date

        return
    def genTable(self, feeSet):
        templist = self.__myList.copy()
        processedRec = {} #to record processed settlement
        for onePos in templist:
            instrument = onePos['合约']
            buyHolding = 0
            sellHolding = 0
            if instrument not in processedRec:
                if '买' in onePos['买/卖']:
                    buyHolding = int(onePos['持仓数量'])
                else:
                    sellHolding = int(onePos['持仓数量'])
                getWord = re.compile(u'[a-zA-Z]+');
                futureHead = getWord.findall(onePos['合约'])
                temp_partid = self.__FutToPartid[futureHead[0].upper()]
                temp_clientid = self.__FutToClientid[futureHead[0].upper()]

                oneTabRow = [temp_partid, temp_clientid, onePos['合约'], float(onePos['结算价']), 0, 0, 0, 0, 0, 0, 0.00, 0.00,buyHolding, sellHolding, float(onePos['保证金占用']), float(onePos['持仓盯市盈亏']), 0.00 ]
                processedRec[instrument] = oneTabRow
            else:
                if '买' in onePos['买/卖']:
                    buyHolding = int(onePos['持仓数量'])
                else:
                    sellHolding = int(onePos['持仓数量'])
                existRow = processedRec[instrument]
                existRow[12] += buyHolding
                existRow[13] += sellHolding
                if float(onePos['保证金占用']) > existRow[15]:
                    existRow[14] = float(onePos['保证金占用'])
                existRow[15] += float(onePos['持仓盯市盈亏'])
                processedRec[instrument] = existRow

        for instrument in feeSet:
            tRec = feeSet[instrument]
            if tRec['合约'] in processedRec:
                tFee = round(tRec['手续费'],2)
                processedRec[tRec['合约']][16] = tFee
            else:
                buyHolding = tRec['买']
                sellHolding = tRec['卖']
                #float(onePos['结算价'])
                tclearPrice = round(tRec['卖成交价'],2)
                #float(onePos['保证金占用'])
                tmargin = 0.0
                #float(onePos['持仓盯市盈亏'])
                tactual = 0.0
                getWord = re.compile(u'[a-zA-Z]+');
                futureHead = getWord.findall(tRec['合约'])
                temp_partid = self.__FutToPartid[futureHead[0].upper()]
                temp_clientid = self.__FutToClientid[futureHead[0].upper()]
                tFee = round(tRec['手续费'],2)
                tRow = [temp_partid, temp_clientid, tRec['合约'], tclearPrice, 0, 0, 0, 0, 0, 0, 0.00, 0.00,buyHolding, sellHolding, tmargin, tactual, tFee]
                processedRec[tRec['合约']] = tRow

        self.__genTable = processedRec.values()

        return
    def addFeeSet(self, feeSet):
        self.genTable(feeSet)
        return
    def writeDbf(self, path):
        temphead = {}
        temphead['结算会员号'] = str(self.__account)
        table = dbf.Table(path)
        table.open()
        copyTable = table.new('./output/'+ self.__account + '_' + self.__mydate + '_settlementdetail.dbf')
        copyTable.open()

        rowVals = []
        if hasattr(self, '_positions__genTable'):
            rowVals = self.__genTable

        for oneRow in rowVals:
            tempRecord = []
            for data in oneRow:
                tempRecord.append(str(data))
            if Gdebug:
                print(tuple(tempRecord))
            #table.append(tuple(tempRecord))
            copyTable.append(tuple(tempRecord))
            #tempRecord.clear()

        copyTable.close()
        table.close()


        return
    def writeTxt(self, path, strHeader):
        HSName = '中信期货有限公司标准合约结算明细表'
        #keys = self.__myList[0].keys()
        templist = self.__myList.copy()
        txtTable = PrettyTable(['结算会员号', '客户编码', '合约', '结算价', '买开成交量', '买平成交量', '买成交量合计', '卖开成交量', '卖平成交量', '卖成交量合计', '买入成交额', '卖出成交额', '买持仓量合计', '卖持仓量合计', '交易保证金', '当日盈亏', '手续费'])
        txtTable.set_style(DEFAULT)
        txtTable.align = "r"
        txtTable.padding_width = 1
        txtTable.float_format = .2
        #|  合约  | 买/卖 | 持仓数量 |  开仓均价  |  结算价  | 持仓盯市盈亏 |    保证金占用   |  投保  |
        tempTabRows = {}
        for onePos in templist:
            instrument = onePos['合约']
            buyHolding = 0
            sellHolding = 0
            if not instrument in tempTabRows:
                if '买' in onePos['买/卖']:
                    buyHolding = int(onePos['持仓数量'])
                else:
                    sellHolding = int(onePos['持仓数量'])
                oneTabRow = ['0000', '00000000', onePos['合约'], float(onePos['结算价']), 0, 0, 0, 0, 0, 0, 0.00, 0.00,buyHolding, sellHolding, float(onePos['保证金占用']), float(onePos['持仓盯市盈亏']), 0.00 ]
                tempTabRows[instrument] = oneTabRow
            else:
                if '买' in onePos['买/卖']:
                    buyHolding = int(onePos['持仓数量'])
                else:
                    sellHolding = int(onePos['持仓数量'])
                existRow = tempTabRows[instrument]
                existRow[12] += buyHolding
                existRow[13] += sellHolding
                if float(onePos['保证金占用']) > existRow[15]:
                    existRow[14] = float(onePos['保证金占用'])
                existRow[15] += float(onePos['持仓盯市盈亏'])
                tempTabRows[instrument] = existRow
        rowVals = tempTabRows.values()

        for rowVal in rowVals:
                txtTable.add_row(rowVal)
        if Gdebug:
            print(txtTable)


        if os.path.isfile(path):
            os.remove(path)
            print(path + " removed!"  )
        f = open(path, 'a')
        f.write(HSName)
        f.write('\n')
        f.write('\n')
        f.write(strHeader)
        f.write('\n')
        f.write(txtTable.get_string())
        f.write('\n')


        f.close()

        return
class aggregateFutures:
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
    def __init__(self, textList = []):


        self.settlementTxt = []
        self.accountTxt = []
        self.depositTxt = []
        self.transactionTxt = []
        self.realizeTxt = []
        self.deliveryTxt = []
        self.positionsDetailTxt = []
        self.positionsTxt = []

        self.__myPath = './txt/'
        self.__myDBFPath = './template'
        self.__company = ''
        self.__accNum = ''
        self.__date = ''
        self.__strHeader = ''
        self.name = 'test'
        #self.__myAcc = account()
        # self.__myPositionsDetail = positionsDetail()
        self.__myPositions = positions()
        # self.__myTransaction = transaction()
        # self.__myClientCapitalDetail = ClientCapitalDetail()
        self.__GenTxt = False

        print('__init__')
        block = []
        for line in textList:
            if (not line) or (line.strip('\n') == '') or (self.isGarbageLine(line)):
                continue
            else:
                block.append(line.strip())

        self.cleanRawTxt(block)
        return

    def getPositions(self):


        return self.__myPositions.getPostions()

    def cleanDBFTables(self, path):
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='UTF8') #改变标准输出的默认编码
        files = os.listdir(path)
        for file in files:
            file = path + '/' + file
            if os.path.isdir(file):
                continue
            else:
                #srcFile = open(file, 'r')
                table = dbf.Table(file)
                table.open()
                for record in table:
                    #record.decode("ascii").encode("utf-8")

                    if Gdebug:
                        print('-'*200)
                        print(record)
                        print('-'*200)
                    dbf.delete(record)

                table.pack()
                if Gdebug:
                    print('+'*200)
                for record in table:
                    if Gdebug:
                        print(record)
                table.close()



    print("\n cleanTables exit!")
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
    operator = {'结算单':setSettlementTxt, '资金状况':setAccountTxt, '持仓明细':setPositionsDetailTxt,
                '持仓汇总':setPositionsTxt, '成交明细':setTransactionTxt, '平仓明细':setRealizeTxt, '交割明细':setDeliveryTxt,
                '中信期货':setCompTxt, '出入金明细':setDepositNWithdraw}
    keyWords = ['结算单', '资金状况', '持仓明细', '持仓汇总', '成交明细', '平仓明细', '出入金明细', '中信期货']

    def cleanRawTxt(self,txt):
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
                                self.operator.get(tempkey)(self, txtcup)
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