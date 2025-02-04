import requests
import pandas as pd
def CallEarningsInfo(ticker_symbol):
    api_key = 'PFPDC6Y4H9E66Z4U'  # 替换为你的API密钥
    symbol = ticker_symbol  # 替换为你感兴趣的股票代码
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    # 解析财报数据
    earnings_data = data.get('quarterlyEarnings', [])
    earnings_df = pd.DataFrame(earnings_data)
    
    # print(earnings_df)
    return earnings_df
