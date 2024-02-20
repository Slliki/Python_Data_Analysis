import backtrader as bt
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 定义策略
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),  # 移动平均线窗口大小
        ('rsiperiod', 14),  # RSI指标的周期
        ('rsiupper', 70),  # RSI过高阈值，超过此值可能考虑卖出
        ('rsilower', 30),  # RSI过低阈值，低于此值可能考虑买入
    )

    # 日志记录
    # 若传入了dt参数，则使用传入的日期，否则使用数据本身的日期
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 保持对收盘价的引用，即只关注收盘价这一列并用于策略
        self.dataclose = self.datas[0].close

        # 初始化order（订单状态），buyprice（买入价格）和buycomm（买入佣金）
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 用于买卖策略的指标
        # sma: 简单移动平均线
        # rsi: 相对强弱指标
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)
        self.rsi = bt.indicators.RSI(self.datas[0], period=self.params.rsiperiod)

        # 仅用于绘图的指标
        # subplot=True表示在原图上叠加显示，否则单独显示
        # plot=False表示不用于作图，但是可以用于策略逻辑
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25, subplot=False)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        bt.indicators.StochasticSlow(self.datas[0], subplot=True)
        bt.indicators.MACDHisto(self.datas[0], subplot=True)
        bt.indicators.ATR(self.datas[0], plot=False)

    # 每个订单状态发生变化时被Backtrader调用（例如，订单被接受、完成或取消）。它用于处理订单状态的变化，如记录订单完成时的价格和佣金，以及在订单被取消或拒绝时输出相关信息。
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # 若order状态为Completed，则进行下一步判断
        if order.status in [order.Completed]:
            # 订单已经完成，若为买入，则记录买入价格price，总花费cost（value），佣金comm
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                # 更新买入价格和佣金
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            # 若为卖出，则记录卖出价格price，总收入value，佣金comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        # 若order状态为Canceled/Margin/Rejected，则记录订单取消/保证金不足/拒绝
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # 重置订单状态
        self.order = None

    # 一个trade是一次完整的买入和卖出过程，该函数用于记录交易的盈利情况
    def notify_trade(self, trade):
        # 若trade不是空且trade不是已经关闭 则退出该函数
        if not trade.isclosed:
            return
        # 若trade已经关闭，则记录交易的毛利润pnl和净利润pnlcomm
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    # 核心策略执行函数
    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # 若有订单正在进行中，则不进行任何操作
        if self.order:
            return

        # 若没有持有仓位，则进行买入判断
        # 策略逻辑：当价格高于SMA且RSI低于上限时买入；当价格低于SMA且RSI高于下限时卖出
        if not self.position:
            if self.dataclose[0] > self.sma[0] and self.rsi[0] < self.params.rsiupper:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0] and self.rsi[0] > self.params.rsilower:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

if __name__ == '__main__':
    # 创建Cerebro引擎对象
    cerebro = bt.Cerebro()
    start_date = datetime(2022, 1, 3)  # 回测开始时间
    end_date = datetime(2024, 2, 20)  # 回测结束时间

    # 加载数据
    data = bt.feeds.YahooFinanceData(dataname="E:\\Bristol\\mini_project\\JPMorgan_Set01\\AAPL_ohlc.csv",
                                     fromdate=start_date, todate=end_date)

    # 将数据传入回测系统
    cerebro.adddata(data)
    # 设置初始资金和佣金
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # 添加该策略到Cerebro
    cerebro.addstrategy(TestStrategy)
    # 可以使用optstrategy进行参数优化代替addstrategy
    # cerebro.optstrategy(
    #     TestStrategy,
    #     param1=range(10, 20),  # param1将从10遍历到19
    #     param2=[20, 30, 40]    # param2将在这三个值中进行遍历
    # )
    # 增加每次交易的股票数量
    cerebro.addsizer(bt.sizers.FixedSize, stake=70)
    # 运行回测
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # 绘制图表
    cerebro.plot(figuersize=(1000, 500))
