# -*- coding: utf-8 -*-
#                                                          结算单
#
# 账户：12020088808
# 日期：20170216
#资金状况
# 上次结算资金：      4445396.88 								 交割手续费：              0.00
# 出入金：                  0.00 								 期末结存：          4374800.87
# 平仓盈亏：           -26825.00 								 保证金占用：        1323682.95
# 持仓盈亏：           -42600.00 								 可用资金：          3051117.92
# 手续费：               1171.01 								 风险度：                30.26%
#|     合约代码    |    交易所 | 开仓日期| 投/保| 买/卖|  手数 |    开仓价   |    结算价   |   持仓盈亏  |    保证金   |

# --------------------------------------------------------成交明细-------------------------------------------------------
#
# |      合约代码   |    交易所 | 成交日期| 买/卖| 投/保|       成交价|  手数 |  开平 |      手续费   |      成交编号   |
settlement ={'clientID': '账户', 'Date':'日期'}
accShema = {"PreBalance":'上次结算资金', 'DeliveryFee':'交割手续费', 'DepositWithdrawal': '出入金',
            'Balancecf':'期末结存', 'RealizedPL':'平仓盈亏', 'MarginOccupied':'保证金占用', 'MTMPL':'持仓盈亏',
            'FundAvail':'可用资金', 'Fee':'手续费', 'RiskDegree':'风险度'}
# --------------------------------------------------------成交明细-------------------------------------------------------
#
# |      合约代码   |    交易所 | 成交日期| 买/卖| 投/保|       成交价|  手数 |  开平 |      手续费   |      成交编号   |
# --------------------------------------------------------平仓明细-------------------------------------------------------
#
# |     合约代码    | 成交日期| 买/卖|       开仓价|       平仓价|  手数 |  开平 |   平仓盈亏  | 投/保|     成交编号    |
# --------------------------------------------------------持仓汇总-------------------------------------------------------
#
# |     合约代码    |    买/卖|    手数 |       开仓均价  |        结算价   |     持仓盯市盈亏|    保证金占用   |  投/保|
# --------------------------------------------------------持仓明细-------------------------------------------------------
#
# |     合约代码    |    交易所 | 开仓日期| 投/保| 买/卖|  手数 |    开仓价   |    结算价   |   持仓盈亏  |    保证金   |

transactionRecordShema = {'Instrument':'合约代码', 'Exchange':'交易所', 'Date':'成交日期', 'S/H':'投/保', 'B/S':'买/卖', 'Lots':'手数', 'Price':'成交价', 'O/C':'开平', 'Fee':'手续费', 'Trans.No.':'成交编号'}
positionClosed = {'Instrument':'合约代码', 'CloseDate':'成交日期', 'B/S':'买/卖', 'OpenPrice':'开仓价', 'TransPrice':'平仓价', 'Lots':'手数', 'O/C':'开平', 'RealizedP/L':'平仓盈亏', 'S/H':'投/保', 'Trans.No.':'成交编号'}
positionsDetail = {'Instrument':'合约代码', 'Exchange':'交易所', 'Date':'开仓日期', 'S/H':'投/保', 'B/S':'买/卖', 'Lots':'手数', 'OpenPrice':'开仓价', 'SttlToday':'结算价', 'MTMP/L':'持仓盈亏', 'MarginOccupied':'保证金'}
positions = {'Instrument':'合约代码', 'B/S':'买/卖', 'Lots':'手数', 'AvgOpenPrice':'开仓均价', 'SttlToday':'结算价', 'MTMP/L':'持仓盯市盈亏', 'MarginOccupied':'保证金占用', 'S/H':'投/保'}
GStransactionRecord = {'Instrument':'合约代码', 'Exchange':'交易所', 'Date':'成交日期', 'S/H':'投/保', 'B/S':'买/卖', 'Lots':'手数', 'Price':'成交价', 'O/C':'开平', 'Fee':'手续费', 'Trans.No.':'成交编号'}
GSpositionClosed = {'Instrument':'合约代码', 'CloseDate':'成交日期', 'B/S':'买/卖', 'OpenPrice':'开仓价', 'TransPrice':'平仓价', 'Lots':'手数', 'O/C':'开平', 'RealizedP/L':'平仓盈亏', 'S/H':'投/保', 'Trans.No.':'成交编号'}
GSpositionsDetail = {'Instrument':'合约代码', 'Exchange':'交易所', 'Date':'开仓日期', 'S/H':'投/保', 'B/S':'买/卖', 'Lots':'手数', 'OpenPrice':'开仓价', 'SttlToday':'结算价', 'MTMP/L':'持仓盈亏', 'MarginOccupied':'保证金'}
GSpositions = {'Instrument':'合约代码', 'B/S':'买/卖', 'Lots':'手数', 'AvgOpenPrice':'开仓均价', 'SttlToday':'结算价', 'MTMP/L':'持仓盯市盈亏', 'MarginOccupied':'保证金占用', 'S/H':'投/保'}
GSsettlement ={'clientID': '账户', 'Date':'日期'}
GSaccShema = {"PreBalance":'上次结算资金', 'DeliveryFee':'交割手续费', 'DepositWithdrawal': '出入金',
            'Balancecf':'期末结存', 'RealizedPL':'平仓盈亏', 'MarginOccupied':'保证金占用', 'MTMPL':'持仓盈亏',
            'FundAvail':'可用资金', 'Fee':'手续费', 'RiskDegree':'风险度'}
#
# def main():
#
#     print(accShema["PreBalance"])
#     return
# if __name__=="__main__":
#     main()