import time
import numpy as np
import yfinance as yf
import pandas as pd
import warnings
# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)
from matplotlib import pyplot as plt
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def tic():
    global start_time
    start_time = time.time()

# 模拟MATLAB中的toc功能
def toc():
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")

def Main_Calcn(start_date,end_date):
    #  # 获取标普500成分股列表
    # sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
    #  # 替换 BRK.B 为 BRK-B
    # sp500_tickers = [ticker.replace('.', '-') for ticker in sp500_tickers]
     
    #  # 手动添加新的股票代码
    # new_tickers = ['PLTR', 'BTC-USD', 'BAYN.DE','TSM','ASML', 'BYD', 'XIACF', 'ANPDY','XPEV', 'NIO', 'SIEGY', 'NVO', 'VWAGY', 'BMWYY', 'MBGYY', 'BASFY','SAP','ALV.DE']  # 这里添加你想要的新股票代码
    # sp500_tickers.extend(new_tickers)
     
    #  # 去除重复的股票代码
    # sp500_tickers = list(set(sp500_tickers))
    # Alternative 
    # 读取CSV文件 
    df = pd.read_csv('my_list.csv') 
    # 将数据框转换为列表 
    sp500_tickers = df.columns.tolist()

    # ticker_objects = {ticker: yf.Ticker(ticker) for ticker in sp500_tickers}
    stock_data_merged = yf.download(sp500_tickers, start=start_date, end=end_date, interval='1d', progress=False)
    tickers_act = stock_data_merged.columns.get_level_values(1).unique()
    ReturnRatesMerged = pd.DataFrame(index=tickers_act,columns = ['Return Rate of MA05','Return Rate of MA10','Return Rate of MA20','Return Rate of MonthlySIP','Return Rate of WeeklySIP','Distance of Close2BBLowerLim'])
    for ticker in tickers_act:
        tic()
        stock_data = stock_data_merged.xs(ticker, level=1, axis=1)
        # stock_data = stock_data_merged.xs('XIACF', level=1, axis=1)
        stock_data = stock_data.dropna()
        try:
            [_,_,_,ReturnRate_MACD] = MacdReturnCalcn(stock_data)
        except Exception as e:
            ReturnRate_MACD = np.nan
            print(f"Error on MacdReturnCalcn for {ticker}: {e}")
        try:
            [_,_,_,ReturnRate_MA5CrossMA10] = MA05MA10ReturnCalcn(stock_data)
        except Exception as e:
            ReturnRate_MA5CrossMA10 = np.nan
            print(f"Error on MA05MA10ReturnCalcn for {ticker}: {e}")
            
            
        try:
            [_,_,_,ReturnRate_BB,NormalizedDistance_Close2BB] = BollBandsReturnCalcn(stock_data)
        except Exception as e:
            ReturnRate_BB =  np.nan
            NormalizedDistance_Close2BB = ReturnRate_BB 
            print(f"Error on BollBandsReturnCalcn for {ticker}: {e}")
            
        try:    
            [_,_,_,ReturnRate_MonthlySIP,ReturnRate_WeeklySIP] = MonthlyAndWeeklySIPReturnCalcn(stock_data) # 计算按月（周）定投的收益率
        except Exception as e:
            ReturnRate_MonthlySIP=np.nan
            ReturnRate_WeeklySIP = ReturnRate_MonthlySIP
            print(f"Error on MonthlyAndWeeklySIPReturnCalcn for {ticker}: {e}")
        try:    
            [_,_,_,_,_,_,ReturnRate_MA05_WoSell,ReturnRate_MA10_WoSell,ReturnRate_MA20_WoSell,ReturnRate_MA05CrossMA10_WoSell,ReturnRate_MA10CrossMA20_WoSell] = MA_SIPReturnCalcn(stock_data) # 计算按均线定投（只买不卖）的收益率
        except Exception as e:
            ReturnRate_MA05_WoSell=np.nan
            ReturnRate_MA10_WoSell = ReturnRate_MA05_WoSell
            ReturnRate_MA20_WoSell = ReturnRate_MA10_WoSell
            ReturnRate_MA05CrossMA10_WoSell = ReturnRate_MA20_WoSell
            ReturnRate_MA10CrossMA20_WoSell = ReturnRate_MA05CrossMA10_WoSell
            print(f"Error on MA_SIPReturnCalcn for {ticker}: {e}")
        try:
            [_,_,_,_,_,_,_,ReturnRate_MA05,ReturnRate_MA10,ReturnRate_MA20] = MA_Invst_Return_Calcn(stock_data) #计算按照均线投资的收益率(MA05/MA10/MA20)
        except Exception as e:
            print(f"Error on MA_Invst_Return_Calcn for {ticker}: {e}")
            ReturnRate_MA05 = np.nan
            ReturnRate_MA10 = ReturnRate_MA05
            ReturnRate_MA20 = ReturnRate_MA10
        ReturnRatesMerged.at[ticker,'Return Rate of MA05'] = ReturnRate_MA05
        ReturnRatesMerged.at[ticker,'Return Rate of MA10'] = ReturnRate_MA10
        ReturnRatesMerged.at[ticker,'Return Rate of MA20'] = ReturnRate_MA20
        ReturnRatesMerged.at[ticker,'Return Rate of MA5CrossMA10'] = ReturnRate_MA5CrossMA10
        ReturnRatesMerged.at[ticker,'Return Rate of MonthlySIP'] = ReturnRate_MonthlySIP
        ReturnRatesMerged.at[ticker,'Return Rate of WeeklySIP'] = ReturnRate_WeeklySIP
        ReturnRatesMerged.at[ticker,'Return Rate of MA05_WoSell'] = ReturnRate_MA05_WoSell
        ReturnRatesMerged.at[ticker,'Return Rate of MA10_WoSell'] = ReturnRate_MA10_WoSell
        ReturnRatesMerged.at[ticker,'Return Rate of MA20_WoSell'] = ReturnRate_MA20_WoSell
        ReturnRatesMerged.at[ticker,'Return Rate of MA05CrossMA10_WoSell'] = ReturnRate_MA05CrossMA10_WoSell
        ReturnRatesMerged.at[ticker,'Return Rate of MA10CrossMA20_WoSell'] = ReturnRate_MA10CrossMA20_WoSell
        ReturnRatesMerged.at[ticker,'Return Rate of MACD'] = ReturnRate_MACD
        ReturnRatesMerged.at[ticker,'Return Rate of BB'] = ReturnRate_BB
        ReturnRatesMerged.at[ticker,'Distance of Close2BBLowerLim'] = NormalizedDistance_Close2BB
        toc()
    return ReturnRatesMerged
def MonthlyAndWeeklySIPReturnCalcn(stock_data):

    date_range = stock_data.index
    # 找到每个月的第一个工作日
    Monthly_buy_points = date_range.to_series().groupby([date_range.year, date_range.month]).first()
    numStockBought = stock_data.loc[Monthly_buy_points,'Close'][0]/stock_data.loc[Monthly_buy_points,'Close']
    for index in date_range:
        stock_data.at[index,'Monthly SIP Return Rate'] = (sum(numStockBought[0:sum(stock_data.loc[index].name>=Monthly_buy_points)])*stock_data.loc[index,'Close']-sum(stock_data.loc[index].name>=Monthly_buy_points)*stock_data.loc[Monthly_buy_points,'Close'][0]) / (sum(stock_data.loc[index].name>=Monthly_buy_points)*stock_data.loc[Monthly_buy_points,'Close'][0])*100
    SIP_Returns_Monthly = stock_data['Monthly SIP Return Rate'][-1]  
    
    stock_data['Year'] = date_range.year
    stock_data['Week']=date_range.isocalendar().week
    # 找到每年每周的第一个工作日
    Weekly_buy_points = stock_data.groupby(['Year', 'Week']).apply(lambda x: x.index.min())
    numStockBought = stock_data.loc[Weekly_buy_points,'Close'][0]/stock_data.loc[Weekly_buy_points,'Close']
    for index in date_range:
        stock_data.at[index,'Weekly SIP Return Rate'] = (sum(numStockBought[0:sum(stock_data.loc[index].name>=Weekly_buy_points)])*stock_data.loc[index,'Close']-sum(stock_data.loc[index].name>=Weekly_buy_points)*stock_data.loc[Weekly_buy_points,'Close'][0]) / (sum(stock_data.loc[index].name>=Weekly_buy_points)*stock_data.loc[Weekly_buy_points,'Close'][0])*100
    SIP_Returns_Weekly = stock_data['Weekly SIP Return Rate'][-1]  
    
    return stock_data,Monthly_buy_points,Weekly_buy_points,SIP_Returns_Monthly,SIP_Returns_Weekly

def MA_SIPReturnCalcn(stock_data):
    # 计算5日均线
    stock_data['MA5'] = stock_data['Close'].rolling(window=5).mean()
    stock_data['MA10'] = stock_data['Close'].rolling(window=10).mean()
    stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
    golden_cross_data_MA05 = stock_data[((stock_data['Close'] > stock_data['MA5']) &(stock_data['Close'].shift(1) < stock_data['MA5'].shift(1)))|((stock_data['Close'] > stock_data['MA5'])&(stock_data['Close'].shift(1) == stock_data['MA5'].shift(1))&(stock_data['Open'].shift(1) < stock_data['MA5'].shift(1)))|((stock_data['Open'].shift(1)<stock_data['MA5'].shift(1))&(stock_data['Close'].shift(1)<=stock_data['MA5'].shift(1))&(stock_data['Open']>stock_data['MA5'])&(stock_data['Close']>=stock_data['MA5']))]
    golden_cross_data_MA10 = stock_data[((stock_data['Close'] > stock_data['MA10']) &(stock_data['Close'].shift(1) < stock_data['MA10'].shift(1)))|((stock_data['Close'] > stock_data['MA10'])&(stock_data['Close'].shift(1) == stock_data['MA10'].shift(1))&(stock_data['Open'].shift(1) < stock_data['MA10'].shift(1)))|((stock_data['Open'].shift(1)<stock_data['MA10'].shift(1))&(stock_data['Close'].shift(1)<=stock_data['MA10'].shift(1))&(stock_data['Open']>stock_data['MA10'])&(stock_data['Close']>=stock_data['MA10']))]
    golden_cross_data_MA20 = stock_data[((stock_data['Close'] > stock_data['MA20']) &(stock_data['Close'].shift(1) < stock_data['MA20'].shift(1)))|((stock_data['Close'] > stock_data['MA20'])&(stock_data['Close'].shift(1) == stock_data['MA20'].shift(1))&(stock_data['Open'].shift(1) < stock_data['MA20'].shift(1)))|((stock_data['Open'].shift(1)<stock_data['MA20'].shift(1))&(stock_data['Close'].shift(1)<=stock_data['MA20'].shift(1))&(stock_data['Open']>stock_data['MA20'])&(stock_data['Close']>=stock_data['MA20']))]
    _,golden_cross_data_MA05CrossMA10,_ = return_rate_calcn_common_part_V2(stock_data,'MA5','MA10','MA5CrossMA10 Return Rate')
    _,golden_cross_data_MA10CrossMA20,_ = return_rate_calcn_common_part_V2(stock_data,'MA10','MA20','MA10CrossMA20 Return Rate')
     # index_temp = np.where(stock_data.index[index]>=golden_cross_data_copy.index)[0]
    # index_temp = np.where(stock_data.index==golden_cross_data_MA05.index)
    stock_data.at[golden_cross_data_MA05.index,'BoughtNumber_Stock_MA05'] =  golden_cross_data_MA05['Close'][0]/golden_cross_data_MA05['Close']
    stock_data.at[golden_cross_data_MA10.index,'BoughtNumber_Stock_MA10'] =  golden_cross_data_MA10['Close'][0]/golden_cross_data_MA10['Close']
    stock_data.at[golden_cross_data_MA20.index,'BoughtNumber_Stock_MA20'] =  golden_cross_data_MA20['Close'][0]/golden_cross_data_MA20['Close']
    stock_data.at[golden_cross_data_MA05CrossMA10.index,'BoughtNumber_Stock_MA05CrossMA10'] =  golden_cross_data_MA05CrossMA10['Close'][0]/golden_cross_data_MA05CrossMA10['Close']
    stock_data.at[golden_cross_data_MA10CrossMA20.index,'BoughtNumber_Stock_MA10CrossMA20'] =  golden_cross_data_MA10CrossMA20['Close'][0]/golden_cross_data_MA10CrossMA20['Close']

    for index_temp in stock_data.index:
        stock_data.at[index_temp,'Return_Rate_MA05'] = (stock_data.loc[:index_temp,'BoughtNumber_Stock_MA05'].sum()*stock_data.loc[index_temp,'Close']-(stock_data.loc[:index_temp,'BoughtNumber_Stock_MA05']*stock_data.loc[:index_temp,'Close']).sum())/(stock_data.loc[:index_temp,'BoughtNumber_Stock_MA05']*stock_data.loc[:index_temp,'Close']).sum()*100
        stock_data.at[index_temp,'Return_Rate_MA10'] = (stock_data.loc[:index_temp,'BoughtNumber_Stock_MA10'].sum()*stock_data.loc[index_temp,'Close']-(stock_data.loc[:index_temp,'BoughtNumber_Stock_MA10']*stock_data.loc[:index_temp,'Close']).sum())/(stock_data.loc[:index_temp,'BoughtNumber_Stock_MA10']*stock_data.loc[:index_temp,'Close']).sum()*100
        stock_data.at[index_temp,'Return_Rate_MA20'] = (stock_data.loc[:index_temp,'BoughtNumber_Stock_MA20'].sum()*stock_data.loc[index_temp,'Close']-(stock_data.loc[:index_temp,'BoughtNumber_Stock_MA20']*stock_data.loc[:index_temp,'Close']).sum())/(stock_data.loc[:index_temp,'BoughtNumber_Stock_MA20']*stock_data.loc[:index_temp,'Close']).sum()*100
        stock_data.at[index_temp,'Return_Rate_MA05CrossMA10'] = (stock_data.loc[:index_temp,'BoughtNumber_Stock_MA05CrossMA10'].sum()*stock_data.loc[index_temp,'Close']-(stock_data.loc[:index_temp,'BoughtNumber_Stock_MA05CrossMA10']*stock_data.loc[:index_temp,'Close']).sum())/(stock_data.loc[:index_temp,'BoughtNumber_Stock_MA05CrossMA10']*stock_data.loc[:index_temp,'Close']).sum()*100
        stock_data.at[index_temp,'Return_Rate_MA10CrossMA20'] = (stock_data.loc[:index_temp,'BoughtNumber_Stock_MA10CrossMA20'].sum()*stock_data.loc[index_temp,'Close']-(stock_data.loc[:index_temp,'BoughtNumber_Stock_MA10CrossMA20']*stock_data.loc[:index_temp,'Close']).sum())/(stock_data.loc[:index_temp,'BoughtNumber_Stock_MA10CrossMA20']*stock_data.loc[:index_temp,'Close']).sum()*100
    
    FinalReturnRate_MA05 = stock_data['Return_Rate_MA05'][-1]
    FinalReturnRate_MA10 = stock_data['Return_Rate_MA10'][-1]
    FinalReturnRate_MA20 = stock_data['Return_Rate_MA20'][-1]
    FinalReturnRate_MA05CrossMA10 = stock_data['Return_Rate_MA05CrossMA10'][-1]
    FinalReturnRate_MA10CrossMA20 = stock_data['Return_Rate_MA10CrossMA20'][-1]
    
    return stock_data,golden_cross_data_MA05,golden_cross_data_MA10,golden_cross_data_MA20,golden_cross_data_MA05CrossMA10,golden_cross_data_MA10CrossMA20,FinalReturnRate_MA05,FinalReturnRate_MA10,FinalReturnRate_MA20,FinalReturnRate_MA05CrossMA10,FinalReturnRate_MA10CrossMA20


def MA_Invst_Return_Calcn(stock_data):

    # 计算5日均线
    stock_data['MA5'] = stock_data['Close'].rolling(window=5).mean()
    stock_data['MA10'] = stock_data['Close'].rolling(window=10).mean()
    stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data,golden_cross_data_MA05_filtered,death_cross_data_MA05_filtered = return_rate_calcn_common_part(stock_data,'MA5','MA5','MA5 Return Rate')
    stock_data,golden_cross_data_MA10_filtered,death_cross_data_MA10_filtered = return_rate_calcn_common_part(stock_data,'MA10','MA10','MA10 Return Rate')
    stock_data,golden_cross_data_MA20_filtered,death_cross_data_MA20_filtered = return_rate_calcn_common_part(stock_data,'MA20','MA20','MA20 Return Rate')
    
    FinalReturnRate_MA05 = stock_data['MA5 Return Rate'][-1]
    FinalReturnRate_MA10 = stock_data['MA10 Return Rate'][-1]
    FinalReturnRate_MA20 = stock_data['MA20 Return Rate'][-1]
    return stock_data,golden_cross_data_MA05_filtered,death_cross_data_MA05_filtered,golden_cross_data_MA10_filtered,death_cross_data_MA10_filtered,golden_cross_data_MA20_filtered,death_cross_data_MA20_filtered,FinalReturnRate_MA05,FinalReturnRate_MA10,FinalReturnRate_MA20

def BollBandsReturnCalcn(stock_data):
    stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['STD20'] = stock_data['Close'].rolling(window=20).std()
    stock_data['BBUpperLim'] = (stock_data['MA20']+2*stock_data['STD20'])
    stock_data['BBBottomLim'] = (stock_data['MA20']-2*stock_data['STD20'])
    try:
        stock_data,golden_cross_data_filtered,death_cross_data_filtered  = return_rate_calcn_common_part(stock_data,'BBBottomLim','BBUpperLim','BB Return Rate')
        FinalReturnRate_BB = stock_data['BB Return Rate'][-1]
    except Exception as e:
        FinalReturnRate_BB =  np.nan
        print(f"Error on BollBandsReturnCalcn: {e}") 
    Distance_BBLowLim2CloseFinal_norm = (stock_data['Close'][-1]-(stock_data['MA20'][-1]-2*stock_data['STD20'][-1]))/max((stock_data['MA20'][-1]-2*stock_data['STD20'][-1]),0.01)
    return stock_data,golden_cross_data_filtered,death_cross_data_filtered,FinalReturnRate_BB,Distance_BBLowLim2CloseFinal_norm    
def MacdReturnCalcn(stock_data):
    # Calculate the short-term EMA (12 days)
    stock_data['EMA12'] = stock_data['Close'].ewm(span=12, adjust=False).mean()
    # Calculate the long-term EMA (26 days)
    stock_data['EMA26'] = stock_data['Close'].ewm(span=26, adjust=False).mean()
    # Calculate MACD line
    stock_data['MACD'] = stock_data['EMA12'] - stock_data['EMA26']
    # Calculate Signal line (9-day EMA of MACD)
    stock_data['Signal'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()
    stock_data,golden_cross_data_MACD,death_cross_data_MACD = return_rate_calcn_common_part_V2(stock_data,'MACD','Signal','MACD Return Rate')
    FinalReturnRate_MACD = stock_data['MACD Return Rate'][-1]
    return stock_data,golden_cross_data_MACD,death_cross_data_MACD,FinalReturnRate_MACD
def MA05MA10ReturnCalcn(stock_data):
    # Calculate the Moving Average Lines
    stock_data['MA5'] = stock_data['Close'].rolling(window=5).mean()
    stock_data['MA10'] = stock_data['Close'].rolling(window=10).mean()
    stock_data,golden_cross_data_MA5CrossMA10,death_cross_MA5CrossMA10 = return_rate_calcn_common_part_V2(stock_data,'MA5','MA10','MA5CrossMA10 Return Rate')
    FinalReturnRate_MA5CrossMA10 = stock_data['MA5CrossMA10 Return Rate'][-1]
    return stock_data,golden_cross_data_MA5CrossMA10,death_cross_MA5CrossMA10,FinalReturnRate_MA5CrossMA10
# 交替插针数组A和B
def filter_dataframes(df_a, df_b):
    # 使用 .copy() 方法创建 DataFrame 的副本
    df_a_copy = df_a.copy()
    df_b_copy = df_b.copy()
    df_a_copy['source'] = 'A'
    df_b_copy['source'] = 'B'
    df_combined = pd.concat([df_a_copy, df_b_copy]).sort_index()   
    for i in range(1, len(df_combined)):
        if df_combined.iloc[i]['source'] == df_combined.iloc[i-1]['source']:
            if df_combined.iloc[i]['source']=='A':
                df_a_copy=df_a_copy.drop(df_combined.index[i])
            else:
                df_b_copy=df_b_copy.drop(df_combined.index[i])
    df_a_copy = df_a_copy.drop(columns='source')
    df_b_copy = df_b_copy.drop(columns='source')
    return df_a_copy,df_b_copy
def return_rate_calcn_common_part(stock_data,columnName_goldenCross,columnName_deathCross,returnRateLabel):
    # 查找金叉死叉位置
    golden_cross_data = stock_data[((stock_data['Close'] > stock_data[columnName_goldenCross]) &(stock_data['Close'].shift(1) < stock_data[columnName_goldenCross].shift(1)))|((stock_data['Close'] > stock_data[columnName_goldenCross])&(stock_data['Close'].shift(1) == stock_data[columnName_goldenCross].shift(1))&(stock_data['Open'].shift(1) < stock_data[columnName_goldenCross].shift(1)))|((stock_data['Open'].shift(1)<stock_data[columnName_goldenCross].shift(1))&(stock_data['Close'].shift(1)<=stock_data[columnName_goldenCross].shift(1))&(stock_data['Open']>stock_data[columnName_goldenCross])&(stock_data['Close']>=stock_data[columnName_goldenCross]))]
    death_cross_data = stock_data[((stock_data['Close'] < stock_data[columnName_deathCross]) & (stock_data['Close'].shift(1) > stock_data[columnName_deathCross].shift(1)))|((stock_data['Close'] < stock_data[columnName_deathCross])&(stock_data['Close'].shift(1) == stock_data[columnName_deathCross].shift(1))&(stock_data['Open'].shift(1) > stock_data[columnName_deathCross].shift(1)))|((stock_data['Open'].shift(1)>stock_data[columnName_deathCross].shift(1))&(stock_data['Close'].shift(1)>=stock_data[columnName_deathCross].shift(1))&(stock_data['Open']<stock_data[columnName_deathCross])&(stock_data['Close']<=stock_data[columnName_deathCross]))]

    while golden_cross_data.index[0] > death_cross_data.index[0]: 
        death_cross_data=death_cross_data.drop(death_cross_data.index[0])
    [golden_cross_data_filtered, death_cross_data_filtered] = filter_dataframes(golden_cross_data,death_cross_data)

        
    # 使用 .copy() 方法创建 DataFrame 的副本
    golden_cross_data_copy = golden_cross_data_filtered.copy()


    # 计算按照死叉金叉的股价交易的卖出价格和买入股数    
    PriceAtSell = np.hstack([death_cross_data_filtered['Close'].shift(1,fill_value=golden_cross_data_copy['Close'][0]).values,death_cross_data_filtered['Close'][-1]])  
    golden_cross_data_copy['Stock Number to Buy'] = np.cumprod(PriceAtSell[0:len(golden_cross_data_copy)]/golden_cross_data_copy['Close'])
       
    for index in range(len(stock_data)):
        index_temp = np.where(stock_data.index[index]>=golden_cross_data_copy.index)[0]
        if index_temp.size == 0:
            stock_data.at[stock_data.index[index],returnRateLabel] = 0
        elif max(index_temp)>len(death_cross_data_filtered)-1:
            stock_data.at[stock_data.index[index],returnRateLabel] = (golden_cross_data_copy['Stock Number to Buy'][max(index_temp)]*stock_data['Close'][index]-golden_cross_data_copy['Close'][0])/golden_cross_data_copy['Close'][0]*100
        elif stock_data.index[index] <= death_cross_data_filtered.index[max(index_temp)]:
            stock_data.at[stock_data.index[index],returnRateLabel] = (golden_cross_data_copy['Stock Number to Buy'][max(index_temp)]*stock_data['Close'][index]-golden_cross_data_copy['Close'][0])/golden_cross_data_copy['Close'][0]*100
        else:
            stock_data.at[stock_data.index[index],returnRateLabel] = stock_data[returnRateLabel][index-1]
    return stock_data,golden_cross_data_filtered,death_cross_data_filtered 

# 计算MACD的金叉死叉和计算对应的买入卖出投资回报率
def return_rate_calcn_common_part_V2(stock_data,NameobjectSignal,NamebaseSignal,returnRateLabel):
    stock_data['Crossover'] = stock_data[NameobjectSignal] - stock_data[NamebaseSignal]
    # Identify the points where crossover happens
    stock_data['Signal_Temp'] = 0  # Initialize signal column
    stock_data.loc[stock_data['Crossover'] > 0, 'Signal_Temp'] = 1  # Bullish signal
    stock_data.loc[stock_data['Crossover'] < 0, 'Signal_Temp'] = -1  # Bearish signal
    stock_data['Cross'] = stock_data['Signal_Temp'].diff()
    # Find golden crosses and death crosses
    golden_crosses_data = stock_data[stock_data['Cross'] == 2]
    death_crosses_data = stock_data[stock_data['Cross'] == -2]
    
    while golden_crosses_data.index[0] > death_crosses_data.index[0]: 
        death_crosses_data=death_crosses_data.drop(death_crosses_data.index[0])
    [golden_cross_data_filtered, death_cross_data_filtered] = filter_dataframes(golden_crosses_data,death_crosses_data)
    # golden_cross_data_filtered,death_cross_data_filtered = golden_crosses_data,death_crosses_data
    # 使用 .copy() 方法创建 DataFrame 的副本
    golden_cross_data_copy = golden_cross_data_filtered.copy()
    # 计算按照死叉金叉的股价交易的卖出价格和买入股数    
    PriceAtSell = np.hstack([death_cross_data_filtered['Close'].shift(1,fill_value=golden_cross_data_copy['Close'][0]).values,death_cross_data_filtered['Close'][-1]])  
    golden_cross_data_copy['Stock Number to Buy'] = np.cumprod(PriceAtSell[0:len(golden_cross_data_copy)]/golden_cross_data_copy['Close'])
       
    for index in range(len(stock_data)):
        index_temp = np.where(stock_data.index[index]>=golden_cross_data_copy.index)[0]
        if index_temp.size == 0:
            stock_data.at[stock_data.index[index],returnRateLabel] = 0
        elif max(index_temp)>len(death_cross_data_filtered)-1:
            stock_data.at[stock_data.index[index],returnRateLabel] = (golden_cross_data_copy['Stock Number to Buy'][max(index_temp)]*stock_data['Close'][index]-golden_cross_data_copy['Close'][0])/golden_cross_data_copy['Close'][0]*100
        elif stock_data.index[index] <= death_cross_data_filtered.index[max(index_temp)]:
            stock_data.at[stock_data.index[index],returnRateLabel] = (golden_cross_data_copy['Stock Number to Buy'][max(index_temp)]*stock_data['Close'][index]-golden_cross_data_copy['Close'][0])/golden_cross_data_copy['Close'][0]*100
        else:
            stock_data.at[stock_data.index[index],returnRateLabel] = stock_data[returnRateLabel][index-1]
    
    
    return stock_data,golden_cross_data_filtered,death_cross_data_filtered
    
# ReturnRateRes = Main_Calcn('2024-01-01','2025-01-08')




