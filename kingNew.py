# -*- coding: utf-8 -*-

import os
import re
import datetime

from decimal import *
from prettytable import *
import dbf

Gdebug = False

def clearPath(path):
    files = os.listdir(path)
    for file in files:
        file = path + '/' + file
        if os.path.isdir(file):
            continue
        else:
            #srcFile = open(file, 'r')
            os.remove(file)




    print("\n cleanTables exit!")
    return
def cleanDBFTables(path):
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

def writeTxt(str, path):
    f = open(path, 'a')
    f.write(str)
    f.close()
    return
class deposit_Withdraw:
    __myName = ''
    def clear(self):

        return
    def __init__(self):
        print(" __init__(deposit_Withdraw)")
        return

class account:
    __myName = ''
    __Initialed = False
    __Balance_bf = 0.00
    __Deposit = 0.00
    __Realized = 0.00
    __MTM = 0.00
    __Commission = 0.00
    __Delivery_Fee = 0.00
    __Balance_cf = 0.00
    __Margin_Occupied = 0.00
    __Fund_Avail = 0.00
    __Risk_Degree = 0.00
    __Currency = 'CNY'
    __account = 0
    __mydate = ''
    __ChgInFund = 0.0
    __Payment = 0.0
    def clear(self):

        return
    def __init__(self):
        self.__myName = ''
        self.__Initialed = False
        self.__Balance_bf = 0.00
        self.__Deposit = 0.00
        self.__Realized = 0.00
        self.__MTM = 0.00
        self.__Commission = 0.00
        self.__Delivery_Fee = 0.00
        self.__Balance_cf = 0.00
        self.__Margin_Occupied = 0.00
        self.__Fund_Avail = 0.00
        self.__Risk_Degree = 0.00
        self.__Currency = 'CNY'
        self.__account = 0
        self.__mydate = ''
        self.__ChgInFund = 0.0
        self.__Payment = 0.0
        print(" __init__(self)")
        return
    def setAccNdate(self, acc, date):
        self.__account = acc
        self.__mydate = date
        return

    def set(self, txt = []):
        self.__myName = '资金状况'
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




        self.__Balance_bf = float(NameToValue['上次结算金'])
        self.__Delivery_Fee = float(NameToValue['交割手续费'])
        self.__Deposit = float(NameToValue['出 入 金'])
        self.__Balance_cf = float(NameToValue['期末结存'])
        self.__Realized = float(NameToValue['平仓盈亏'])
        self.__Margin_Occupied = float(NameToValue['保证金占用'])
        self.__MTM = float(NameToValue['持仓盈亏'])
        self.__Fund_Avail = float(NameToValue['可用资金'])
        self.__Commission = float(NameToValue['手续费'])
        self.__Risk_Degree = float(NameToValue['风险度'])
        self.__Currency = 'CNY'
        self.__ChgInFund = 0.00 + self.__MTM - self.__Commission -self.__Payment
        self.__Initialed = True
        return
    def writeDbf(self, path):
        temphead = {}
        temphead['结算会员号'] = str(self.__account)
        table = dbf.Table(path)
        table.open()
        copyTable = table.new('./output/'+ self.__account + '_' + self.__mydate + '_capital.dbf')
        copyTable.open()


        rows = []
        rows.append((temphead['结算会员号'], '上一交易日实有货币资金余额', str(self.__Balance_bf)))
        rows.append((temphead['结算会员号'],'加：当日收入资金', str(self.__Deposit)))
        rows.append((temphead['结算会员号'], '当日盈亏', str(self.__MTM)))
        rows.append((temphead['结算会员号'],'减：当日付出资金', str(self.__Payment)))
        rows.append((temphead['结算会员号'], '手续费', str(self.__Commission)))
        rows.append((temphead['结算会员号'], '其中：交易手续费', str(self.__Commission)))
        rows.append((temphead['结算会员号'], '结算手续费', '0.00'))
        rows.append((temphead['结算会员号'],'交割手续费', '0.00'))
        rows.append((temphead['结算会员号'], '移仓手续费', '0.00'))
        rows.append((temphead['结算会员号'], '当日实有货币资金余额', str(self.__Balance_cf)))
        rows.append((temphead['结算会员号'],'其中：交易保证金', str(self.__Margin_Occupied)))
        rows.append((temphead['结算会员号'],  '结算准备金', str(self.__Fund_Avail)))
        rows.append((temphead['结算会员号'],  '减：交易保证金', str(self.__Margin_Occupied)))
        rows.append((temphead['结算会员号'],  '当日结算准备金余额', str(self.__Fund_Avail)))
        rows.append((temphead['结算会员号'],  '加：申报划入金额', '0.00'))
        rows.append((temphead['结算会员号'],  '减：申报划出金额', '0.00'))
        rows.append((temphead['结算会员号'],  '下一交易日开仓准备金', str(self.__Fund_Avail)))
        rows.append((temphead['结算会员号'], '其它', '-' ))
        rows.append((temphead['结算会员号'], '应收手续费', str(self.__Commission )))
        rows.append( (temphead['结算会员号'], '实有货币资金变动', str(float(self.__MTM) + float(self.__Realized )) ))
        rows.append((temphead['结算会员号'], '其中：交易保证金变动', '0.00' ))
        rows.append((temphead['结算会员号'], '结算准备金变动', '0.00'))

        s =  r'上一交易日实有货币资金余额'
        #s.decode('UTF-8')
        #table.append( ('13887', '上一交易日实有货币资金余额', '10000.00') )
        for datum in rows:
            #table.append(datum)
            copyTable.append(datum)

        copyTable.close()
        table.close()
        return
    def writeTxt(self, path, strHeader):
        tempTableName = '中信期货有限公司结算会员资金状况表'
        if Gdebug:
            print(str(tempTableName))
        temphead = {}

        #temphead['结算会员号'] = self.__account[0:-2]
        temphead['结算会员号'] = self.__account
        temphead['结算会员名称'] = '中信期货(0018)'
        temphead['资金账号'] = self.__account
        temphead['账号属性'] = '经纪'
        temphead['结算日期'] = self.__mydate
        #print(temphead.items())

        strheader = ['结算会员号: ' + temphead['结算会员号'], '结算会员名称: ' + temphead['结算会员名称'], '资金账号: ' + temphead['资金账号'], '账号属性: ' + temphead['账号属性'], '结算日期: ' + temphead['结算日期'] ]
        if Gdebug:
            print(strheader)
        headTable = PrettyTable(strheader)
        headTable.set_style(PLAIN_COLUMNS)
        headTable.padding_width = 0
        headTable.add_row(['', '', '', '', ''])
        if Gdebug:
            print(headTable)

        txtTable = PrettyTable(['项目                                                                                  ', '金额'])
        txtTable.set_style(DEFAULT)
        txtTable.align["项目                                                                                  "] = "l"
        txtTable.align["金额"] = 'r'
        txtTable.padding_width = 1
        txtTable.add_row(['上一交易日实有货币资金余额', self.__Balance_bf])
        txtTable.add_row(['加：当日收入资金', self.__Deposit])
        txtTable.add_row(['当日盈亏', self.__MTM])
        txtTable.add_row(['减：当日付出资金', self.__Payment])
        txtTable.add_row(['手续费', self.__Commission])
        txtTable.add_row(['其中：交易手续费', self.__Commission])
        txtTable.add_row(['结算手续费', '0.00'])
        txtTable.add_row(['交割手续费', '0.00'])
        txtTable.add_row(['移仓手续费', '0.00'])
        txtTable.add_row(['当日实有货币资金余额', self.__Balance_cf])
        txtTable.add_row(['其中：交易保证金', self.__Margin_Occupied])
        txtTable.add_row(['结算准备金', self.__Fund_Avail])
        txtTable.add_row(['减：交易保证金', self.__Margin_Occupied])
        txtTable.add_row(['当日结算准备金余额', self.__Fund_Avail])
        txtTable.add_row(['加：申报划入金额', '0.00'])
        txtTable.add_row(['减：申报划出金额', '0.00'])
        txtTable.add_row(['下一交易日开仓准备金', self.__Fund_Avail])
        txtTable.add_row(['其它', '-'])
        txtTable.add_row(['应收手续费', self.__Commission])
        txtTable.add_row(['实有货币资金变动', float(self.__MTM) + float(self.__Realized)])
        txtTable.add_row(['其中：交易保证金变动', '0.00'])
        txtTable.add_row(['结算准备金变动', '0.00'])

        if Gdebug:
            print(txtTable)
            print('\n')
            print('收入与付出资金明细栏')
        z = PrettyTable(["单据号                        ", "名称                                                    ", "金额"])
        z.set_style(DEFAULT)
        z.hrules = ALL
        #z.border = False
        z.padding_width = 150
        z.add_row(['', '', ''])
        if Gdebug:
            print(z)

        if os.path.isfile(path):
            os.remove(path)
            print(path + " removed!"  )
        f = open(path, 'a')
        f.write(tempTableName)
        f.write('\n')
        f.write('\n')
        f.write(headTable.get_string())
        f.write('\n')
        f.write(txtTable.get_string())
        f.write('\n')
        f.write('\n')
        f.write('收入与付出资金明细栏')
        f.write('\n')
        f.write(z.get_string())
        f.close()
        return


class positionsDetail:
    __myName = ''
    __keyWords = ['交易所', '合约', '开仓日期', '投/保', '买/卖', '持仓量', '开仓价', '结算价', '盯市盈亏', '保证金']
    __recList = []
    __account = 0
    __mydate = ''
    def setAccNdate(self, acc, date):
        self.__account = acc
        self.__mydate = date
        return
    def clear(self):

        return
    def __init__(self):
        self.__myName = ''
        self.__keyWords = ['交易所', '合约', '开仓日期', '投/保', '买/卖', '持仓量', '开仓价', '结算价', '盯市盈亏', '保证金']
        self.__recList = []
        self.__account = 0
        self.__mydate = ''
        self.__myName = '持仓明细'
        return
    def set(self, txt = []):
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
                self.__recList.append(temp)
                list.append(temp)
        if Gdebug:
            print(self.__recList)
            print(list)
        return
    def writeDbf(self, path):
        #table = dbf.Table(path)
        #table.open()
        #copyTable = table.new('./output/'+ self.__account + '_' + self.__mydate + '_capital.dbf')
        #copyTable.open()
        print('DBF 持仓明细 pass')
        return
    def writeTxt(self, path):
        print('持仓明细 pass')
        return
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
    def __init__(self, posAeg = {}):
        self.__posAeg = posAeg
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
        return
    def setAccNdate(self, acc, date):
        self.__account = acc
        self.__mydate = date

        return
    def getPeakValDir(self, futureID):
        ans = ''
        if futureID in self.__posAeg:
            aPos = self.__posAeg[futureID]
            ans = aPos['单边最大方向']
        else:
            print('计算错误， 合约号不在总持仓中：' + futureID)
        return ans
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
                temp_Margin = 0
                #temp_Margin = float(onePos['保证金占用'])
                if self.getPeakValDir(onePos['合约']) in onePos['买/卖']:
                    temp_Margin = float(onePos['保证金占用'])
                oneTabRow = [temp_partid, temp_clientid, onePos['合约'], float(onePos['结算价']), 0, 0, 0, 0, 0, 0, 0.00, 0.00,buyHolding, sellHolding, temp_Margin, float(onePos['持仓盯市盈亏']), 0.00 ]
                processedRec[instrument] = oneTabRow
            else:
                if '买' in onePos['买/卖']:
                    buyHolding = int(onePos['持仓数量'])
                else:
                    sellHolding = int(onePos['持仓数量'])

                existRow = processedRec[instrument]
                existRow[12] += buyHolding
                existRow[13] += sellHolding
                if self.getPeakValDir(onePos['合约']) in onePos['买/卖']:
                    temp_Margin = float(onePos['保证金占用'])
                    existRow[14] = temp_Margin
                # if float(onePos['保证金占用']) > existRow[15]:
                #     existRow[14] = float(onePos['保证金占用'])
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
class transaction:#成交明细
    __name = '成交明细'

    __myList = []
    IDToMultiplier = {}
    __account = 0
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
    def __init__(self, acc, date):
        self.__name = '成交明细'

        self.__myList = []
        self.IDToMultiplier = {}
        self.__account = 0
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
        self.__myName = 'ClientCapitalDetail'
        self.__account = acc
        self.__mydate = date
        self.__myList.clear()
        return
    def setAccNdate(self, acc, date):
        self.__account = acc
        self.__mydate = date
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
        self.__name = '成交明细'

        self.__myList = []
        self.IDToMultiplier = {}
        self.__account = 0
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
        self.__myName = 'ClientCapitalDetail'
        self.__account = 0
        #self.__mydate = 0
        self.__myName = '持仓汇总'
        if Gdebug:
            print(self.__myName)
        self.readConfig()
        self.__myList.clear()
        return
    #计算持仓汇总, settelmentDetail持仓汇总
    def computeSetDet(self):

        locList = self.__myList[:]
        setDet = {}
        #getcontext().prec = 6
        #getcontext().rounding = ROUND_FLOOR

        for node in locList:
            if node["合约"] not in setDet:
                tempSDNode = {}
                tempSDNode['卖'] = 0
                tempSDNode['买'] = 0
                tempSDNode['卖成交价'] = 0
                tempSDNode['买成交价'] = 0
                if '买' in node['买/卖']:
                    tempSDNode['买'] = int(node['手数'])
                    tempSDNode['买成交价'] = Decimal(node['成交价'])
                else:
                    tempSDNode['卖'] = int(node['手数'])
                    tempSDNode['卖成交价'] = Decimal(node['成交价'])
                tempSDNode['手续费'] = Decimal(node['手续费'])
                tempSDNode['合约'] = node['合约']
                tempSDNode['投/保'] = node['投/保']
                setDet[node['合约']] = tempSDNode

            else:
                tempSDNode = setDet[node['合约']]
                #print(tempSDNode)
                if '买' in node['买/卖']:
                    oldBuyAvg = tempSDNode['买成交价']
                    oldBuySum = tempSDNode['买']
                    nodeBuyAvg = Decimal(node['成交价'])
                    nodeBuySum = int(node['手数'])
                    newBuyAvg = oldBuyAvg * oldBuySum + nodeBuyAvg * nodeBuySum
                    newBuyAvg = newBuyAvg / (oldBuySum + nodeBuySum)
                    tempSDNode['买成交价'] = newBuyAvg
                    tempSDNode['买'] += int(node['手数'])
                else:
                    oldSellAvg = tempSDNode['卖成交价']
                    oldSellSum = tempSDNode['卖']
                    nodeSellAvg = Decimal(node['成交价'])
                    nodeSellSum = int(node['手数'])
                    newSellAvg = oldSellAvg * oldSellSum + nodeSellAvg * nodeSellSum
                    newSellAvg = newSellAvg / (oldSellSum + nodeSellSum)

                    tempSDNode['卖成交价'] = newSellAvg
                    tempSDNode['卖'] += int(node['手数'])
                tempSDNode['手续费'] += Decimal(node['手续费'])

                print("===========================================")
                print(setDet[node['合约']])



        return setDet
    def getFeeSet(self):

        return
    def set(self, txt = []):
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
        return
    def writeDbf(self, path):

        tempTradeList = self.__myList.copy()
        table = dbf.Table(path)
        table.open()
        copyTable = table.new('./output/'+ self.__account + '_' + self.__mydate + '_Trade.dbf')
        copyTable.open()
        tempTime = "9:30:00"
        timedelta = datetime.timedelta(minutes=1)
        pivotTime = datetime.datetime.strptime(tempTime,'%H:%M:%S')
        pivotOrderid = 400000
        for oneTrade in tempTradeList:
            futureID = re.compile(u'[a-zA-Z]+');
            try:
                tFuture = futureID.findall(oneTrade['合约'].upper())
            except KeyError as e:
                print(e)
            else:
                if Gdebug:
                    print('++++++++++++++')
            TradeAmount = int(oneTrade['手数']) * float(oneTrade['成交价']) * self.IDToMultiplier[tFuture[0]]
            getWord = re.compile(u'[a-zA-Z]+');
            futureHead = getWord.findall(oneTrade['合约'])
            temp_partid = self.__FutToPartid[futureHead[0].upper()]
            temp_clientid = self.__FutToClientid[futureHead[0].upper()]
            temp_Userid = self.__customer_Userid["Userid"]
            strTime = pivotTime.strftime('%X')
            pivotTime = pivotTime + timedelta
            strOrderid = str(pivotOrderid)
            pivotOrderid = pivotOrderid + 1

            if len(oneTrade['成交编号']) > 12:
                oneTabTrade = (temp_partid, temp_clientid, oneTrade['合约'], oneTrade['成交编号'][-12:], oneTrade['手数'], oneTrade['成交价'], str(TradeAmount), strTime, oneTrade['买/卖'], oneTrade['开平'], strOrderid, temp_Userid)
            else:

                oneTabTrade = (temp_partid, temp_clientid, oneTrade['合约'], oneTrade['成交编号'], oneTrade['手数'], oneTrade['成交价'], str(TradeAmount), strTime, oneTrade['买/卖'], oneTrade['开平'], strOrderid, temp_Userid)
            #table.append(oneTabTrade)
            #print(oneTabTrade)
            #print('====================')
            copyTable.append(oneTabTrade)






        copyTable.close();
        table.close()
        return
    def writeTxt(self, path, strHeader):
        HSName = '中信期货有限公司成交单'

        #交易会员  客户编码    合约          撮合编号  成交量      成交价      成交金额  成交时间  买/卖 开/平  报单号        席位号
        tempTradeList = self.__myList.copy()

        txtTable = PrettyTable(['交易会员', '客户编码', '合约', '撮合编号', '成交量', '成交价', '成交金额', '成交时间', '买/卖', '开/平', '报单号', '席位号'])
        txtTable.set_style(DEFAULT)
        txtTable.align = "r"
        txtTable.padding_width = 1
        txtTable.float_format = .2
        #| 成交日期 | 交易所 |  合约  | 买/卖 | 投/保 |  成交价  |  手数 |开平 |  手续费  |  成交编号  |
        for oneTrade in tempTradeList:
            futureID = re.compile(u'[a-zA-Z]+');
            tFuture = futureID.findall(oneTrade['合约'].upper())
            TradeAmount = int(oneTrade['手数']) * float(oneTrade['成交价']) * self.IDToMultiplier[tFuture[0]]
            oneTabTrade = ['2051', '00000000', oneTrade['合约'], oneTrade['成交编号'], oneTrade['手数'], oneTrade['成交价'], TradeAmount, '00:00:00', oneTrade['买/卖'], oneTrade['开平'], '000000', '000000']
            txtTable.add_row(oneTabTrade)
        if Gdebug:
            print(txtTable.get_string())

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
class Delivery:
    __account = 0
    __mydate = ''
    def clear(self):

        return
    def __init__(self, acc, date):
        __myName = 'Delivery'
        self.__account = acc
        self.__mydate = date
        return
    def setAccNdate(self, acc, date):
        self.__account = acc
        self.__mydate = date
        return
    def writeDbf(self, path):
        table = dbf.Table(path)
        table.open()
        copyTable = table.new('./output/'+ self.__account + '_' + self.__mydate + '_Delivery.dbf')
        copyTable.open()
        table.close()
        copyTable.close()
        print('DBF 持仓明细 pass')
        return

    def writeTxt(self, path, strHeader):
        HSName = '中信期货有限公司交割情况表'
        #交割合约  结算会员号    结算会员简称  资金账号    属性            交割结算价        买入量        卖出量    交割手续费
        txtTable = PrettyTable(['交割合约', '结算会员号', '结算会员简称', '资金账号', '属性', '交割结算价', '买入量', '卖出量', '交割手续费'])
        txtTable.set_style(DEFAULT)
        txtTable.align = "r"
        txtTable.padding_width = 1
        txtTable.float_format = .2
        txtTable.add_row(['', '', '', '', '', '','', '', '',])

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
class ClientCapitalDetail:
    __account = 0
    __mydate = ''
    __tableList = []
    def clear(self):

        return
    def __init__(self):
        self.__account = 0
        self.__mydate = ''
        self.__tableList = []
        __myName = 'ClientCapitalDetail'
        self.__tableList.clear()
        return
    # def __init__(self, acc, date):
    #     __myName = 'ClientCapitalDetail'
    #     self.__account = acc
    #     self.__mydate = date
    #     return
    def setAccNdate(self, acc, date):
        self.__account = acc
        self.__mydate = date
        return
    def set(self, txt = []):
        self.__myName = '资金状况'
        NameToValue = {}
        tHeaderLine = txt[1]
        phanzi=re.compile(u'[\u4e00-\u9fa5]+');
        tHeader = phanzi.findall(tHeaderLine)

        for line in txt[2:]:



            if '|' not in line:
                continue
            if '共' in line:
                continue
            str = line.split('|')
            tempLine = ''.join(str)
            #phanzi=re.compile(u'[\u4e00-\u9fa5]+');
            index = 0
            tHeaderLen = tHeader.__len__()
            data = {}
            for val in str[1:-1]:

                if index < tHeaderLen:
                    data[tHeader[index]] = val.strip()
                index += 1
            self.__tableList.append(data)




        return
    def process(self, txt = []):

        return
    def writeDbf(self, path):
        table = dbf.Table(path)
        table.open()
        copyTable = table.new('./output/'+ self.__account + '_' + self.__mydate + '_ClientCapitalDetail.dbf')
        copyTable.open()
        for item in self.__tableList:
            if Gdebug:
                print(item)
            withdraw = item['出金']
            deposit = item['入金']
            moneySum = float(deposit) - float(withdraw)
            oneRow = (self.__account, "0018", self.__account, str(moneySum),"0020", item['说明'])
            copyTable.append(oneRow)

        #oneTabTrade = (temp_partid, temp_clientid, oneTrade['合约'], oneTrade['成交编号'], oneTrade['手数'], oneTrade['成交价'], str(TradeAmount), strTime, oneTrade['买/卖'], oneTrade['开平'], strOrderid, temp_Userid)

        #copyTable.append(oneTabTrade)

        #copyTable.open()
        table.close()
        copyTable.close()
        print('DBF 持仓明细 pass')
        return
    def writeTxt(self, path, strHeader):
        HSName = '分项资金明细表'
        #资金账号    交易会员号        交易编码          金额      资金类型  资金类型备注
        txtTable = PrettyTable(['资金账号', '交易会员号', '交易编码', '金额', '资金类型', '资金类型备注'])
        txtTable.set_style(DEFAULT)
        txtTable.align = "r"
        txtTable.padding_width = 1
        txtTable.float_format = .2
        txtTable.add_row(['', '', '', '', '', ''])

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
class kingNew:
    __myPath = './txt/'
    __myDBFPath = './template'
    __company = ''
    __accNum = ''
    __date = ''
    __strHeader = ''
    name = 'test'
    __myAcc = account()
    __myPositionsDetail = positionsDetail()
    __myPositions = positions()
    __myTransaction = transaction()
    __myClientCapitalDetail = ClientCapitalDetail()
    __GenTxt = False
    #
    keyWords = ['结算单', '资金状况', '持仓明细', '持仓汇总', '成交明细', '平仓明细', '出入金明细', '中信期货']
    settlementTxt = []
    accountTxt = []
    depositTxt = []
    transactionTxt = []
    realizeTxt = []
    deliveryTxt = []
    positionsDetailTxt = []
    positionsTxt = []
    def clear(self):
        self.__myAcc.clear()
        self.__myPositions.clear()
        self.__myPositionsDetail.clear()
        self.__myPositions.clear()
        self.__myTransaction.clear()
        #del self

        self.settlementTxt.clear()
        self.accountTxt.clear()
        self.depositTxt.clear()
        self.transactionTxt.clear()
        self.realizeTxt.clear()
        self.deliveryTxt.clear()
        self.positionsDetailTxt.clear()
        self.positionsTxt.clear()
        return
    def setAccNdate(self, txt = []):
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

        if '账户' in NameToValue:
            self.__accNum = NameToValue['账户']
        elif  '客户号' in NameToValue:
            self.__accNum = NameToValue['客户号']
        else:
            print('账户没有正确解析')
            self.__accNum = 'NULL'
        self.__date = NameToValue['日期']
        #结算会员:13887    结算会员名称:中信期货(0018)   结算日期:20161213
        #self.__strHeader = '结算会员: ' + self.__accNum[0:-2] + '       结算会员名称:中信期货(0018)' + '      结算日期:' + self.__date
        self.__strHeader = '结算会员: ' + self.__accNum + '       结算会员名称:中信期货(0018)' + '      结算日期:' + self.__date
        return
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
    operator = {'结算单':setSettlementTxt, '资金状况':setAccountTxt, '持仓明细':setPositionsDetailTxt,
                '持仓汇总':setPositionsTxt, '成交明细':setTransactionTxt, '平仓明细':setRealizeTxt, '交割明细':setDeliveryTxt,
                '中信期货':setCompTxt, '出入金明细':setDepositNWithdraw}
    # def __init__(self):
    #     print('__init__')
    #     print(self.name)
    #     return
    def __init__(self, textList = [], posAeg = {}):

        #需要将类开头的类变量在这里初始化，变为对象独有的一个变量

        self.__posAeg = posAeg.copy()
        self.settlementTxt = []
        self.accountTxt = []
        self.depositTxt = []
        self.transactionTxt = []
        self.realizeTxt = []
        self.deliveryTxt = []
        self.positionsDetailTxt = []
        self.positionsTxt = []

        #clearPath('./output')
        self.__myAcc = account()
        self.__myPositionsDetail = positionsDetail()
        self.__myPositions = positions(self.__posAeg)
        self.__myTransaction = transaction()
        self.__myClientCapitalDetail = ClientCapitalDetail()
        print('__init__')
        block = []
        for line in textList:
            if line.strip('\n') == '' or '---' in line:
                continue
            else:
                block.append(line.strip())

        self.cleanRawTxt(block)
        return

    def getBlockType(self, line):

        for key in self.keyWords:
            if key in line:
                if Gdebug:
                    print(key)

        return
    def cleanRawTxt(self,txt):
        cleanTxt = []
        txtcup = []
        tempkey = ''
        newBlock = False
        cleanDBFTables(self.__myDBFPath)
        GenTxt = False
        for line in txt:
            for key in self.keyWords:
                if key in line:
                    if txtcup:
                        if tempkey in self.operator:
                            self.operator.get(tempkey)(self, txtcup)
                        txtcup.clear()
                    tempkey = key
                    newBlock = True
                    break

            txtcup.append(line)

        if txtcup:
            self.operator.get(tempkey)(self, txtcup)
            txtcup.clear()
        if self.settlementTxt:
            self.setAccNdate(self.settlementTxt)
        if self.accountTxt:
            self.__myAcc.set(self.accountTxt)
            self.__myAcc.setAccNdate(self.__accNum, self.__date)

        if self.positionsDetailTxt:
            self.__myPositionsDetail.set(self.positionsDetailTxt)

        tempFeeSet = {}
        #将每条交易的交易费用加起来
        if self.transactionTxt:
            self.__myTransaction.set(self.transactionTxt)
            tempFeeSet = self.__myTransaction.computeSetDet()
            self.__myTransaction.setAccNdate(self.__accNum, self.__date)

        #需要将交易费用加上
        if self.positionsTxt:
            self.__myPositions.set(self.positionsTxt)
            self.__myPositions.setAccNdate(self.__accNum, self.__date)

            self.__myPositions.addFeeSet(tempFeeSet)
        elif self.transactionTxt and tempFeeSet:
            self.__myPositions.setAccNdate(self.__accNum, self.__date)
            self.__myPositions.addFeeSet(tempFeeSet)
            print("")
        else:
            print('')

        if self.depositTxt:

            self.__myClientCapitalDetail.setAccNdate(self.__accNum, self.__date)
            self.__myClientCapitalDetail.set(self.depositTxt)



        self.writeHSBill()
        return




    def writeHSBill(self):
        if self.positionsTxt or self.transactionTxt:
            self.__myPositions.writeDbf(self.__myDBFPath + '/settlementdetail.dbf')
        if self.transactionTxt:
            self.__myTransaction.writeDbf(self.__myDBFPath + '/Trade.dbf')
        if self.depositTxt:
            self.__myClientCapitalDetail.writeDbf(self.__myDBFPath + '/clientcapitaldetail.dbf')
        if self.accountTxt:
            self.__myAcc.writeDbf(self.__myDBFPath + '/capital.dbf')

        # if self.__GenTxt:
        #     self.__myAcc.writeTxt(self.__myPath + 'Capital.txt', self.__strHeader)
        #     self.__myClientCapitalDetail.writeTxt(self.__myPath + 'ClientCapitalDetail.txt', self.__strHeader)
        #     self.__myPositions.writeTxt(self.__myPath + 'SettlementDetail.txt', self.__strHeader)
        #     self.__myTransaction.writeTxt(self.__myPath + 'Trade.txt', self.__strHeader)
        tempDelivery = Delivery(self.__accNum, self.__date)
        tempDelivery.writeDbf(self.__myDBFPath + '/delivery.dbf')
        if self.__GenTxt:
            tempDelivery.writeTxt(self.__myPath + 'Delivery.txt', self.__strHeader)
        return