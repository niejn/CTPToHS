# -*- coding: utf-8 -*-
settlement ={'clientID': '账户', 'Date':'日期'}
accShema = {"PreBalance":'上次结算资金', 'DeliveryFee':'交割手续费', 'DepositWithdrawal': '出入金',
            'Balancecf':'期末结存', 'RealizedPL':'平仓盈亏', 'MarginOccupied':'保证金占用', 'MTMPL':'持仓盈亏',
            'FundAvail':'可用资金', 'Fee':'手续费', 'RiskDegree':'风险度'}


transactionRecordShema = {'Instrument':'合约代码', 'Exchange':'交易所', 'Date':'成交日期', 'S/H':'投/保', 'B/S':'买/卖', 'Lots':'手数', 'Price':'成交价', 'O/C':'开平', 'Fee':'手续费', 'Trans.No.':'成交编号'}
positionClosed = {'Instrument':'合约代码', 'CloseDate':'成交日期', 'B/S':'买/卖', 'OpenPrice':'开仓价', 'TransPrice':'平仓价', 'Lots':'手数', 'O/C':'开平', 'RealizedP/L':'平仓盈亏', 'S/H':'投/保', 'Trans.No.':'成交编号'}
positionsDetail = {'Instrument':'合约代码', 'Exchange':'交易所', 'Date':'开仓日期', 'S/H':'投/保', 'B/S':'买/卖', 'Lots':'手数', 'OpenPrice':'开仓价', 'SttlToday':'结算价', 'MTMP/L':'持仓盈亏', 'MarginOccupied':'保证金'}
positions = {'Instrument':'合约代码', 'B/S':'买/卖', 'Lots':'手数', 'AvgOpenPrice':'开仓均价', 'SttlToday':'结算价', 'MTMP/L':'持仓盯市盈亏', 'MarginOccupied':'保证金占用', 'S/H':'投/保'}
GStransactionRecord = {'Instrument':'合约代码', 'Exchange':'交易所', 'Date':'成交日期', 'S/H':'投/保', 'B/S':'买/卖', 'Lots':'手数', 'Price':'成交价', 'O/C':'开平', 'Fee':'手续费', 'Trans.No.':'成交编号'}
GSpositionClosed = {'Instrument':'合约代码', 'CloseDate':'成交日期', 'B/S':'买/卖', 'OpenPrice':'开仓价', 'TransPrice':'平仓价', 'Lots':'手数', 'O/C':'开平', 'RealizedP/L':'平仓盈亏', 'S/H':'投/保', 'Trans.No.':'成交编号'}
GSpositionsDetail = {'Instrument':'合约代码', 'Exchange':'交易所', 'Date':'开仓日期', 'S/H':'投/保', 'B/S':'买/卖', 'Lots':'手数', 'OpenPrice':'开仓价', 'SttlToday':'结算价', 'MTMP/L':'持仓盈亏', 'MarginOccupied':'保证金'}
GSpositions = {'Instrument':'合约代码', 'B/S':'买/卖', 'Lots':'手数', 'AvgOpenPrice':'开仓均价', 'SttlToday':'结算价', 'MTMP/L':'持仓盯市盈亏', 'MarginOccupied':'保证金占用', 'S/H':'投/保'}
GParentSettlement ={'clientID': '账户', 'Date':'日期'}
GSaccShema = {"PreBalance":'上次结算资金', 'DeliveryFee':'交割手续费', 'DepositWithdrawal': '出入金',
            'Balancecf':'期末结存', 'RealizedPL':'平仓盈亏', 'MarginOccupied':'保证金占用', 'MTMPL':'持仓盈亏',
            'FundAvail':'可用资金', 'Fee':'手续费', 'RiskDegree':'风险度'}
