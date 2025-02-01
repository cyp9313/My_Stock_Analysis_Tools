import yfinance as yf
import warnings
# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
import mplfinance as mpf
from matplotlib import pyplot as plt
from sp500_calc_test import MonthlyAndWeeklySIPReturnCalcn,MA_Invst_Return_Calcn,BollBandsReturnCalcn,MacdReturnCalcn,MA05MA10ReturnCalcn,MA_SIPReturnCalcn
# 设置中文字体
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
# plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
def SIPReturnCalcn(ticker_symbol, start_date, end_date):
    #%% 下载股票数据
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')
    stock_data.columns = stock_data.columns.get_level_values(0)
    #%% 计算按周（月）定投收益和画图
    [stock_data,Monthly_buy_points,Weekly_buy_points,SIP_Returns_Monthly,SIP_Returns_Weekly]=MonthlyAndWeeklySIPReturnCalcn(stock_data)
    # 创建图形和两个子图
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw={'height_ratios': [1, 1, 1]}, figsize=(10, 10),sharex=True)
    # 创建图形和轴对象
    mpf.plot(stock_data, type='candle', volume=False, ax=ax1, show_nontrading=True, returnfig=True, style='charles')
    mpf.plot(stock_data, type='candle', volume=False, ax=ax2, show_nontrading=True, returnfig=True, style='charles')
    # 为每个均线手动添加图例
    ax1.plot(stock_data.index, stock_data['Close'].rolling(window=5).mean(), label='5-Day MAV', color='blue', linestyle='--',linewidth=1)
    ax1.plot(stock_data.index, stock_data['Close'].rolling(window=10).mean(), label='10-Day MAV', color='orange', linestyle='--',linewidth=1)
    ax1.plot(stock_data.index, stock_data['Close'].rolling(window=20).mean(), label='20-Day MAV', color='green', linestyle='--',linewidth=1)
    ax2.plot(stock_data.index, stock_data['Close'].rolling(window=5).mean(), label='5-Day MAV', color='blue', linestyle='--',linewidth=1)
    ax2.plot(stock_data.index, stock_data['Close'].rolling(window=10).mean(), label='10-Day MAV', color='orange', linestyle='--',linewidth=1)
    ax2.plot(stock_data.index, stock_data['Close'].rolling(window=20).mean(), label='20-Day MAV', color='green', linestyle='--',linewidth=1)
    # 在指定位置绘制买入点位置
    ax1.plot(Monthly_buy_points, stock_data.loc[Monthly_buy_points, 'Close'], 'rx', markersize=5,label='Monthly Buy points')
    ax2.plot(Weekly_buy_points, stock_data.loc[Weekly_buy_points, 'Close'], 'bx', markersize=5,label='Weekly Buy points')
  
    ax3.plot(stock_data.index, stock_data['Monthly SIP Return Rate'], 'r', label = 'Monthly SIP Return Rate')
    ax3.plot(stock_data.index, stock_data['Weekly SIP Return Rate'], 'b', label = 'Weekly SIP Return Rate')
    ax3.axhline(y=SIP_Returns_Monthly, color='r', linestyle='--',linewidth=1, label=f'Last Value Monthly SIP Return Rate in %: {SIP_Returns_Monthly:.1f}')
    ax3.axhline(y=SIP_Returns_Weekly, color='b', linestyle='--',linewidth=1, label=f'Last Value Weekly SIP Return Rate in %: {SIP_Returns_Weekly:.1f}')
    print(f'按月定投收益率 %:{SIP_Returns_Monthly:.1f}')
    print(f'按周定投收益率 %:{SIP_Returns_Weekly:.1f}')
    # 显示图例
    for ax in [ax1,ax2,ax3]:
        ax.grid(True)
        ax.legend(loc='best',ncol=1)
    # 设置图表标题
    fig.suptitle(f'{ticker_symbol} Candlestick Chart with Calculation of SIP Return Rates')
    plt.tight_layout()
    plt.show()
    #%% 计算按均线金叉定投收益和画图
    stock_data,golden_cross_data_MA05_filtered,golden_cross_data_MA10_filtered,golden_cross_data_MA20_filtered,golden_cross_data_MA05CrossMA10,golden_cross_data_MA10CrossMA20,FinalReturnRate_MA05,FinalReturnRate_MA10,FinalReturnRate_MA20,FinalReturnRate_MA05CrossMA10,FinalReturnRate_MA10CrossMA20 = MA_SIPReturnCalcn(stock_data)

    # stock_data,golden_cross_data_MA05_filtered,death_cross_data_MA05_filtered,golden_cross_data_MA10_filtered,death_cross_data_MA10_filtered,golden_cross_data_MA20_filtered,death_cross_data_MA20_filtered,FinalReturnRate_MA05,FinalReturnRate_MA10,FinalReturnRate_MA20 = MA_Invst_Return_Calcn(stock_data)
    # stock_data,golden_cross_data_MA05CrossMA10,death_cross_data_MA05CrossMA10,FinalReturnRate_MA05CrossMA10 = MA05MA10ReturnCalcn(stock_data)
    print(f'按MA5定投收益率 %:{FinalReturnRate_MA05:.1f}')
    print(f'按MA10定投收益率 %:{FinalReturnRate_MA10:.1f}')
    print(f'按MA20定投收益率 %:{FinalReturnRate_MA20:.1f}')
    print(f'按MA5和MA10的交叉定投收益率 %:{FinalReturnRate_MA05CrossMA10:.1f}')
    print(f'按MA10和MA20的交叉定投收益率 %:{FinalReturnRate_MA10CrossMA20:.1f}')
    
    # 创建图形和两个子图
    fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, gridspec_kw={'height_ratios': [1, 1, 1, 1, 1, 1]}, figsize=(10, 15),sharex=True)
    # 创建图形和轴对象
    mpf.plot(stock_data, type='candle', volume=False, ax=ax1, show_nontrading=True, returnfig=True, style='charles')
    mpf.plot(stock_data, type='candle', volume=False, ax=ax2, show_nontrading=True, returnfig=True, style='charles')
    mpf.plot(stock_data, type='candle', volume=False, ax=ax3, show_nontrading=True, returnfig=True, style='charles')
    mpf.plot(stock_data, type='candle', volume=False, ax=ax4, show_nontrading=True, returnfig=True, style='charles')
    mpf.plot(stock_data, type='candle', volume=False, ax=ax5, show_nontrading=True, returnfig=True, style='charles')
    # 为每个均线手动添加图例
    ax1.plot(stock_data.index, stock_data['MA5'] , label='5-Day MAV', color='blue', linestyle='--',linewidth=1)
    ax2.plot(stock_data.index, stock_data['MA10'] , label='10-Day MAV', color='orange', linestyle='--',linewidth=1)
    ax3.plot(stock_data.index, stock_data['MA20'] , label='20-Day MAV', color='green', linestyle='--',linewidth=1)
    ax4.plot(stock_data.index, stock_data['MA5'] , label='5-Day MAV', color='blue', linestyle='--',linewidth=1)
    ax4.plot(stock_data.index, stock_data['MA10'] , label='10-Day MAV', color='orange', linestyle='--',linewidth=1)
    ax5.plot(stock_data.index, stock_data['MA10'] , label='10-Day MAV', color='orange', linestyle='--',linewidth=1)
    ax5.plot(stock_data.index, stock_data['MA20'] , label='20-Day MAV', color='green', linestyle='--',linewidth=1)
    # 在指定位置绘制买入和卖出点位置
    ax1.plot(golden_cross_data_MA05_filtered.index, golden_cross_data_MA05_filtered.Close, 'rx', markersize=5,label='MA05 Buy points')
    ax2.plot(golden_cross_data_MA10_filtered.index, golden_cross_data_MA10_filtered.Close, 'rx', markersize=5,label='MA10 Buy points')
    ax3.plot(golden_cross_data_MA20_filtered.index, golden_cross_data_MA20_filtered.Close, 'rx', markersize=5,label='MA20 Buy points')
    ax4.plot(golden_cross_data_MA05CrossMA10.index, golden_cross_data_MA05CrossMA10.Close, 'rx', markersize=5,label='MA05CrossMA10 Buy points')
    ax5.plot(golden_cross_data_MA10CrossMA20.index, golden_cross_data_MA10CrossMA20.Close, 'rx', markersize=5,label='MA10CrossMA20 Buy points')
   
    ax6.plot(stock_data.index, stock_data['Return_Rate_MA05'], 'r', label = 'MA05 SIP Return Rate')
    ax6.plot(stock_data.index, stock_data['Return_Rate_MA10'], 'b', label = 'MA10 SIP Return Rate')
    ax6.plot(stock_data.index, stock_data['Return_Rate_MA20'], 'g', label = 'MA20 SIP Return Rate')
    ax6.plot(stock_data.index, stock_data['Return_Rate_MA05CrossMA10'], 'c', label = 'MA05CrossMA10 SIP Return Rate')
    ax6.plot(stock_data.index, stock_data['Return_Rate_MA10CrossMA20'], 'm', label = 'MA10CrossMA20 SIP Return Rate')
    ax6.axhline(y=FinalReturnRate_MA05, color='r', linestyle='--',linewidth=1, label=f'Last Value MA05 SIP Return Rate in %: {FinalReturnRate_MA05:.1f}')
    ax6.axhline(y=FinalReturnRate_MA10, color='b', linestyle='--',linewidth=1, label=f'Last Value MA10 SIP Return Rate in %: {FinalReturnRate_MA10:.1f}')
    ax6.axhline(y=FinalReturnRate_MA20, color='g', linestyle='--',linewidth=1, label=f'Last Value MA20 SIP Return Rate in %: {FinalReturnRate_MA20:.1f}')
    ax6.axhline(y=FinalReturnRate_MA05CrossMA10, color='c', linestyle='--',linewidth=1, label=f'Last Value MA05CrossMA10 SIP Return Rate in %: {FinalReturnRate_MA05CrossMA10:.1f}')
    ax6.axhline(y=FinalReturnRate_MA10CrossMA20, color='m', linestyle='--',linewidth=1, label=f'Last Value MA10CrossMA20 SIP Return Rate in %: {FinalReturnRate_MA10CrossMA20:.1f}')
    for ax in [ax1,ax2,ax3,ax4,ax5,ax6]:
        ax.grid(True)
        ax.legend(loc='best',ncol=1)
    fig.suptitle(f'{ticker_symbol} Candlestick Chart with Calculation of SIP Return Rates based on MA Lines (no sell)')
    plt.tight_layout()
    plt.show()    
    #%% 计算按均线投资收益和画图
    stock_data,golden_cross_data_MA05_filtered,death_cross_data_MA05_filtered,golden_cross_data_MA10_filtered,death_cross_data_MA10_filtered,golden_cross_data_MA20_filtered,death_cross_data_MA20_filtered,FinalReturnRate_MA05,FinalReturnRate_MA10,FinalReturnRate_MA20 = MA_Invst_Return_Calcn(stock_data)
    stock_data,golden_cross_data_MA05CrossMA10,death_cross_data_MA05CrossMA10,FinalReturnRate_MA05CrossMA10 = MA05MA10ReturnCalcn(stock_data)
    print(f'按MA5定投收益率 %:{FinalReturnRate_MA05:.1f}')
    print(f'按MA10定投收益率 %:{FinalReturnRate_MA10:.1f}')
    print(f'按MA20定投收益率 %:{FinalReturnRate_MA20:.1f}')
    print(f'按MA5和MA10的交叉定投收益率 %:{FinalReturnRate_MA05CrossMA10:.1f}')

    # 创建图形和两个子图
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, gridspec_kw={'height_ratios': [1, 1, 1, 1, 1]}, figsize=(10, 15),sharex=True)
    # 创建图形和轴对象
    mpf.plot(stock_data, type='candle', volume=False, ax=ax1, show_nontrading=True, returnfig=True, style='charles')
    mpf.plot(stock_data, type='candle', volume=False, ax=ax2, show_nontrading=True, returnfig=True, style='charles')
    mpf.plot(stock_data, type='candle', volume=False, ax=ax3, show_nontrading=True, returnfig=True, style='charles')
    mpf.plot(stock_data, type='candle', volume=False, ax=ax4, show_nontrading=True, returnfig=True, style='charles')
    # 为每个均线手动添加图例
    ax1.plot(stock_data.index, stock_data['MA5'] , label='5-Day MAV', color='blue', linestyle='--',linewidth=1)
    ax2.plot(stock_data.index, stock_data['MA10'] , label='10-Day MAV', color='orange', linestyle='--',linewidth=1)
    ax3.plot(stock_data.index, stock_data['MA20'] , label='20-Day MAV', color='green', linestyle='--',linewidth=1)
    ax4.plot(stock_data.index, stock_data['MA5'] , label='5-Day MAV', color='blue', linestyle='--',linewidth=1)
    ax4.plot(stock_data.index, stock_data['MA10'] , label='10-Day MAV', color='orange', linestyle='--',linewidth=1)
    # 在指定位置绘制买入和卖出点位置
    ax1.plot(golden_cross_data_MA05_filtered.index, golden_cross_data_MA05_filtered.Close, 'rx', markersize=5,label='MA05 Buy points')
    ax2.plot(golden_cross_data_MA10_filtered.index, golden_cross_data_MA10_filtered.Close, 'rx', markersize=5,label='MA10 Buy points')
    ax3.plot(golden_cross_data_MA20_filtered.index, golden_cross_data_MA20_filtered.Close, 'rx', markersize=5,label='MA20 Buy points')
    ax4.plot(golden_cross_data_MA05CrossMA10.index, golden_cross_data_MA05CrossMA10.Close, 'rx', markersize=5,label='MA05CrossMA10 Buy points')
    ax1.plot(death_cross_data_MA05_filtered.index, death_cross_data_MA05_filtered.Close, 'bx', markersize=5,label='MA05 Sell points')
    ax2.plot(death_cross_data_MA10_filtered.index, death_cross_data_MA10_filtered.Close, 'bx', markersize=5,label='MA10 Sell points')
    ax3.plot(death_cross_data_MA20_filtered.index, death_cross_data_MA20_filtered.Close, 'bx', markersize=5,label='MA20 Sell points')    
    ax4.plot(death_cross_data_MA05CrossMA10.index, death_cross_data_MA05CrossMA10.Close, 'bx', markersize=5,label='MA05CrossMA10 Sell points') 
   
    ax5.plot(stock_data.index, stock_data['MA5 Return Rate'], 'r', label = 'MA05 SIP Return Rate')
    ax5.plot(stock_data.index, stock_data['MA10 Return Rate'], 'b', label = 'MA10 SIP Return Rate')
    ax5.plot(stock_data.index, stock_data['MA20 Return Rate'], 'g', label = 'MA20 SIP Return Rate')
    ax5.plot(stock_data.index, stock_data['MA5CrossMA10 Return Rate'], 'c', label = 'MA05CrossMA10 SIP Return Rate')
    ax5.axhline(y=FinalReturnRate_MA05, color='r', linestyle='--',linewidth=1, label=f'Last Value MA05 SIP Return Rate in %: {FinalReturnRate_MA05:.1f}')
    ax5.axhline(y=FinalReturnRate_MA10, color='b', linestyle='--',linewidth=1, label=f'Last Value MA10 SIP Return Rate in %: {FinalReturnRate_MA10:.1f}')
    ax5.axhline(y=FinalReturnRate_MA20, color='g', linestyle='--',linewidth=1, label=f'Last Value MA20 SIP Return Rate in %: {FinalReturnRate_MA20:.1f}')
    ax5.axhline(y=FinalReturnRate_MA05CrossMA10, color='c', linestyle='--',linewidth=1, label=f'Last Value MA05CrossMA10 SIP Return Rate in %: {FinalReturnRate_MA05CrossMA10:.1f}')
    for ax in [ax1,ax2,ax3,ax4,ax5]:
        ax.grid(True)
        ax.legend(loc='best',ncol=1)
    fig.suptitle(f'{ticker_symbol} Candlestick Chart with Calculation of SIP Return Rates based on MA Lines')
    plt.tight_layout()
    plt.show()
    #%% 计算按布林带投资收益和画图
    #计算根据布林带投资收益
    [stock_data,golden_cross_data_filtered,death_cross_data_filtered,FinalReturnRate_BB,_]=BollBandsReturnCalcn(stock_data)
    
    print(f'按BB上下轨投资收益率 %:{FinalReturnRate_BB:.1f}')
    # 创建0图形和两个子图
    fig2, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 1]}, figsize=(10, 8),sharex=True)
    # 创建图形和轴对象
    mpf.plot(stock_data, type='candle', volume=False, ax=ax1, show_nontrading=True, returnfig=True, style='charles')
    # 为每个均线手动添加图例
    ax1.plot(stock_data.index, stock_data['Close'].rolling(window=5).mean(), label='5-Day MAV', color='blue', linestyle='--',linewidth=1)
    ax1.plot(stock_data.index, stock_data['Close'].rolling(window=10).mean(), label='10-Day MAV', color='orange', linestyle='--',linewidth=1)
    ax1.plot(stock_data.index, stock_data['Close'].rolling(window=20).mean(), label='20-Day MAV', color='green', linestyle='--',linewidth=1)
    ax1.plot(stock_data.index, stock_data['BBUpperLim'], label='Bolling Band Uppler Lane', color='#ADD8E6', linestyle='--',linewidth=1)
    ax1.plot(stock_data.index, stock_data['BBBottomLim'], label='Bolling Band Lower Lane', color='#ADD8E6', linestyle='--',linewidth=1)

    # 在指定位置绘制买入点位置
    ax1.plot(golden_cross_data_filtered.index, golden_cross_data_filtered.Close, 'rx', markersize=10,label='Buy points')
    ax1.plot(death_cross_data_filtered.index, death_cross_data_filtered.Close, 'bx', markersize=10,label='Sell points')   
       
    ax2.plot(stock_data.index, stock_data['BB Return Rate'], 'r', label = 'BB Return Rate')
    ax2.axhline(y=FinalReturnRate_BB, color='r', linestyle='--',linewidth=1, label=f'Last Value BB Return Rate in %: {FinalReturnRate_BB:.1f}')

    for ax in [ax1,ax2]:
        ax.grid(True)
        ax.legend(loc='best',ncol=1)

    # 设置图表标题
    fig2.suptitle(f'{ticker_symbol} Candlestick Chart with Calculation of BB Return Rates')
    plt.tight_layout()
    plt.show()
    #%% 计算MACD投资收益和画图
    stock_data,golden_cross_data_MACD,death_cross_data_MACD,FinalReturnRate_MACD = MacdReturnCalcn(stock_data)
    # 创建图形和两个子图
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw={'height_ratios': [1, 1, 1]}, figsize=(10, 10),sharex=True)
    # 创建图形和轴对象
    mpf.plot(stock_data, type='candle', volume=False, ax=ax1, show_nontrading=True, returnfig=True, style='charles')
    # 为每个均线手动添加图例
    ax1.plot(stock_data.index, stock_data['Close'].rolling(window=5).mean(), label='5-Day MAV', color='blue', linestyle='--',linewidth=1)
    ax1.plot(stock_data.index, stock_data['Close'].rolling(window=10).mean(), label='10-Day MAV', color='orange', linestyle='--',linewidth=1)
    ax1.plot(stock_data.index, stock_data['Close'].rolling(window=20).mean(), label='20-Day MAV', color='green', linestyle='--',linewidth=1)
    ax2.plot(stock_data.index, stock_data['MACD'], label='MACD Line', color='blue',linewidth=1)
    ax2.plot(stock_data.index, stock_data['Signal'], label='Signal Line', color='orange',linewidth=1)
    # 在指定位置绘制买入点位置
    ax1.plot(golden_cross_data_MACD.index, golden_cross_data_MACD.Close, 'rx', markersize=5,label='MACD Buy points')
    ax1.plot(death_cross_data_MACD.index, death_cross_data_MACD.Close, 'bx', markersize=5,label='MACD Sell points')
    ax2.plot(golden_cross_data_MACD.index, stock_data.loc[golden_cross_data_MACD.index,'MACD'], 'rx', markersize=5,label='MACD Golden points')
    ax2.plot(death_cross_data_MACD.index, stock_data.loc[death_cross_data_MACD.index,'MACD'], 'bx', markersize=5,label='MACD Death points')
  
    ax3.plot(stock_data.index, stock_data['MACD Return Rate'], 'r', label = 'MACD Return Rate')
    ax3.axhline(y=FinalReturnRate_MACD, color='r', linestyle='--',linewidth=1, label=f'Last Value MACD Return Rate in %: {FinalReturnRate_MACD:.1f}')
    print(f'按MACD金叉死叉投资收益率 %:{FinalReturnRate_MACD:.1f}')
    # 显示图例
    for ax in [ax1,ax2,ax3]:
        ax.grid(True)
        ax.legend(loc='best',ncol=1)
    # 设置图表标题
    fig.suptitle(f'{ticker_symbol} Candlestick Chart with Calculation of MACD Return Rates')
    plt.tight_layout()
    plt.show()
#%% 呼叫程序
# SIPReturnCalcn(StockTicker,StartDate,EndDate)
# SIPReturnCalcn('MBGYY','2023-01-01','2024-10-22')

