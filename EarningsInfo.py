import requests
import pandas as pd
def CallEarningsInfo(ticker_symbol):
    api_key = 'PFPDC6Y4H9E66Z4U'  # 替换为你的API密钥
    symbol = ticker_symbol  # 替换为你感兴趣的股票代码
    # url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={api_key}'
    
    # response = requests.get(url)
    # data = response.json()
    
    # # 解析财报数据
    # earnings_data = data.get('quarterlyEarnings', [])
    # earnings_df = pd.DataFrame(earnings_data)
    
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    # 获取财务数据
    trailing_pe = data.get('PERatio')
    forward_pe = data.get('ForwardPE')
    market_cap = data.get('MarketCapitalization')
    peg_ratio = data.get('PEGRatio')
    price_to_sales = data.get('PriceToSalesRatioTTM')
    price_to_book = data.get('PriceToBookRatio')
    # 将市值转换为科学计数法
    market_cap_sci = f'{float(market_cap):.2e}' if market_cap else 'None'

    print(f'{symbol} 的 trailing PE 为: {trailing_pe}')
    print(f'{symbol} 的 forward PE 为: {forward_pe}')
    print(f'{symbol} 的 market cap 为: {market_cap_sci}')
    print(f'{symbol} 的 PEG Ratio 为: {peg_ratio}')
    print(f'{symbol} 的 Price/Sales 为: {price_to_sales}')
    print(f'{symbol} 的 Price/Book 为: {price_to_book}')

    # print(earnings_df)
    # return earnings_df, trailing_pe, forward_pe, market_cap_sci, peg_ratio, price_to_sales, price_to_book
    return trailing_pe, forward_pe, market_cap_sci, peg_ratio, price_to_sales, price_to_book
# earnings_result,_,_,_,_,_,_ = CallEarningsInfo('AAPL')
# print(earnings_result)
