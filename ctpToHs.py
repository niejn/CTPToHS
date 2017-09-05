# -*- coding: utf-8 -*-
# import xdrlib ,sys
# import copy
import os
from datetime import *
import traceback
import pandas as pd
# from KingNewSchema import *
from billRead import *
from childBillRead import  childBill
# import io
import logging
import logging.handlers
import logging.config

#----------------------------------------------------------------------
logging.config.fileConfig('logging.conf')
# root_logger = logging.getLogger('root')
# root_logger.info('root logger')
cth_logger = logging.getLogger('main')
#logger = logging.getLogger('billRead')
cth_logger.info('test main logger')
#logging.ERROR
# bill_logger = logging.getLogger('bill')
# bill_logger.error("This is warning message")





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
def readSingleBill(file):


    if not os.path.isfile(file):
        return
    with open(file, 'rb') as srcFile:
        # textlist = srcFile.readlines()
        content = srcFile.read().decode('utf-8')

        textlist = content.split('\n')

    return textlist

#need read gbk txt error
def readBill(path):
    blockList = []
    files = os.listdir(path)
    file = path + '/' + files[0]
    if not os.path.isfile(file):
        return
    with open(file, 'r') as srcFile:
        textlist = srcFile.readlines()

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
            # srcFile.close()

    return textContainer

def processBill(text):

    return



#read all childBills referencing the same parent
def getChildBill(childBillPath):
    children = []
    for eachPath in childBillPath:
        childTxt = readSingleBill(eachPath)
        cbill = childBill(childTxt)
        children.append(cbill)

    return children

def getChildBillDict(path):
    parentBillSize = 9
    childBillDict = {}
    files = os.listdir(path)
    textContainer = []
    for file in files:
        full_file = path + '/' + file
        if not os.path.isfile(full_file):
            continue
        if file.endswith('txt'):
            #120200889072017-02-16.txt
            if len(file) < parentBillSize:
                raise Exception("Invalid child bill", file)
            pKey = file[:parentBillSize]
            childPath = path + '/' + file
            childPathList = []
            childPathList.append(childPath)
            if pKey in childBillDict:
                childBillDict[pKey].extend(childPathList)
            else:
                childBillDict[pKey] = childPathList

    return childBillDict

def ironing(parentBill, childBills=[]):
    parentPosition = parentBill.positionList
    # for eachPostion in parentPosition:
    #     print(eachPostion)
    #print(parentPosition.columns)
    #df['h-index'] = df.groupby('author')['citations'].transform(lambda x: ( x >= x.rank(ascending=False, method='first') ).sum() )
    #df['h-index'] = df.groupby('author')['citations'].transform(lambda x: ( x >= x.rank(ascending=False, method='first') ).sum() ) ​
    # for index, row in df.iterrows():
    # for index, row in df.iterrows():
    # if row[0]==current_author:
    #     if row[1]>hindex:
    #         hindex+=1
    #df_obj['列名'].astype(int)#转换某列的数据类型
    # parentPosition[]
    # for each_index in parentPosition.index:
    # print(parentPosition.irow(0)  )
    # .iloc[i]
    print(parentPosition.iloc[0])
    print(parentPosition['买持'])
     # 买持     |    买均价   |     卖持
    # list(filter(lambda x:True if x % 3 == 0 else False, range(100)))
    # print df[(df['sex'] == 'Female') & (df['total_bill'] > 20)]
    # parentPosition['较大单边方向'] = parentPosition["买持", '卖持'].transform(lambda buy, sell: True if buy > sell else False )
    df = parentPosition
    # print(df[(df['买持'] > df['卖持'])])
    mask = (parentPosition['买持'] > parentPosition['卖持'])
    parentPosition["较大单边"] = mask
    print(parentPosition["较大单边"])
    print(mask)



    # for index, row in parentPosition.iterrows():
    #     print(index)
    #     print(row)
    #     print(row['合约'])
    # hasattr(object, name)
    for each_child in childBills:
        if hasattr(each_child, 'positionList'):
            child_position = each_child.positionList
        else:
            continue
        print(child_position)
        cmask = (child_position['买/卖'] == '买')
        child_position['持仓方向'] = cmask
        print(child_position)
        for index, row in child_position.iterrows():
            filter = (parentPosition['合约'] == row["合约代码"])
            #make sure that only one row is returned
            # data.irow(0)
            parent_row = parentPosition[filter].iloc[0]
            # if len(parent_row) != 1:
            #     # raise Exception("Invalid level!", level)
            #     raise Exception("More than 1 parent bill row!", len(parent_row))
            # print(len(parent_row))


            # if (parent_row["较大单边"]):
            #     if '买'in row['买/卖']:
            print(row)
            print(parent_row)
            rowDir = row['持仓方向']
            parDir = parent_row["较大单边"]
            if row['持仓方向'] == parent_row["较大单边"]:
                EPSINON = 0.000001
                temp_child_margin = row['保证金占用']
                temp_Parent_margin = parent_row["保证金占用"]
                temp_res = temp_child_margin - temp_Parent_margin
                #bugfix, 如果保证金相等，那么退出来计算，应该考虑手数不相同，保证金相同的情况：
                # if abs(row['保证金占用'] - parent_row["保证金占用"]) <= EPSINON:
                #
                #     continue
                cPos = row['手数']
                if parent_row["较大单边"]:
                    pPos = parent_row["买持"];
                else:
                    pPos = parent_row["卖持"];

                if cPos <= pPos:

                    print(row['保证金占用'])
                    print(parent_row["保证金占用"])
                    # row['保证金占用'] = parent_row["保证金占用"] * cPos * 1.0 / pPos
                    c_margin = parent_row["保证金占用"] * cPos * 1.0 / pPos
                    each_child.positionList.set_value(index, '保证金占用', c_margin)
                    print(each_child.positionList)
                    # parent_row["保证金占用"] -= row['保证金占用']
                    # pPos -= cPos
                    # print(row['保证金占用'])
                    # print(parent_row["保证金占用"])
                    # if parent_row["较大单边"]:
                    #     parent_row["买持"] =  pPos;
                    # else:
                    #     parent_row["卖持"] = pPos ;
                else:
                    raise Exception("child margin occupied is more than parent margin occupied", row['合约代码'])
            else:
                # row['保证金占用'] = 0.0
                child_position.set_value(index, '保证金占用', 0.0)
                each_child.positionList.set_value(index, '保证金占用', 0.0)
                print(child_position)
                # df['c'][1]=4
                # child_position['保证金占用'][index] = 0.0
                #df.set_value('C', 'x', 10)
                # each_child.positionList.set_value('保证金占用', index, 0.0)


    return childBills
def feeReplace(parentBill, childBills=[]):
    if not hasattr(parentBill, 'transList'):
        return childBills
    paTrans = parentBill.transList
    # print(paTrans)
    for each_child in childBills:
        if hasattr(each_child, 'transList'):
            child_trans = each_child.transList
        else:
            continue
        # cmask = (if child_trans['交易所'] == '郑商所': child_trans['成交编号'] = child_trans['成交编号'][4:])
        # child_trans['id'] = child_trans['交易所']transform(lambda )
        # np.where(df.Retention_x == None, df.Retention_y, else df.Retention_x)
        # dfCurrentReportResults['Retention'] =  dfCurrentReportResults.apply(lambda x : x.Retention_y if x.Retention_x == None else x.Retention_x, axis=1)
        child_trans['id'] = child_trans.apply(lambda x : x.成交编号[4:] if x.交易所 == '郑商所' else x.成交编号, axis=1)
        # child_trans['id'] = child_trans.where(child_trans.交易所 == '郑商所', child_trans['成交编号'][4:], child_trans['成交编号'])

        # print(child_trans)
        for index, row in child_trans.iterrows():
            cFieldLen = len(row["id"])
            tRowKey = row["id"]
            tOriginKey = row["id"]
            if cFieldLen < 8:
                tRowKey = tRowKey.zfill(8)
            filter = (paTrans['成交序号'] == tRowKey)
            originFilter = (paTrans['成交序号'] == tOriginKey)
            try:
                temp = paTrans[filter]
                originRes = paTrans[originFilter]
                if len(paTrans[filter]) > 0:
                    parent_row = paTrans[filter].iloc[0]
                elif not originRes.empty:

                    parent_row = originRes.iloc[0]
                else:
                    raise Exception("len(paTrans[filter]) == 0", paTrans['成交序号'])
            except IndexError as e:
                print("Error:")
                print(paTrans['成交序号'])
                print(row["id"])
                traceback.print_exc(file=sys.stdout)
                cth_logger.error(e)

            except Exception as e:
                print("Error:")
                print(paTrans['成交序号'])
                print(row["id"])
                traceback.print_exc(file=sys.stdout)
                cth_logger.error(e)
            # print(parent_row)
            # print(row)
            EPSINON = 0.000001
            print(row)
            if abs(row['手续费'] - parent_row["手续费"]) <= EPSINON:
                continue
            tfee = parent_row["手续费"]
            each_child.transList.set_value(index, '手续费', tfee)
            parse = "--------------------------------------"
            print(parse)
            print(tfee)
            print(row['成交编号'])
            print(parse)
            # print(each_child.transList)

    return childBills
def main():

    path = './txt'
    subAccPath = './subacc';



    childBillDict = getChildBillDict(subAccPath)
    parentAccPath = "./parentAcc"
    pBills = ParentBillList(parentAccPath)
    pBillKeys = pBills.getPBillKeys()
    #childBillDict = getChildBillDict(subAccPath)

    #split the parent bill margin occupied field to fill the child bill margin occupied field
    for eachpbill in pBillKeys:
        if eachpbill in childBillDict:
            parentBill = pBills.getPBill(eachpbill)
            childBillPath = childBillDict[eachpbill]
            childBills = getChildBill(childBillPath)
            #modify the child bills according to the parent bill
            # childBills =
            ironing(parentBill, childBills)
            feeReplace(parentBill, childBills)

            for each_child in childBills:
                # print(each_child.transList)
                # print(each_child.positionList)
                each_child.writeDbf()





    print("\n程序运行正常结束！")
    #raw_input()
    #test = float(input())


    os.system("pause")
    return

if __name__=="__main__":
    main()
