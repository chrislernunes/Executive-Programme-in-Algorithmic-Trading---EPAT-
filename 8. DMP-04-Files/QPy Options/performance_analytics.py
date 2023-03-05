# Compute daily Returns and store it in variable ret
def compute_ret(data): 
    # ret is daily returns
    data['ret'] = data.Close/data.Close.shift(1)-1
    data['strategy_ret'] = data.ret * data.signal.shift(1)
    return data

# Compute Sharpe Ratio and store it in variable sharpe
def rolling_sharpe(data,window):    
    data['sharpe'] = data.strategy_ret.rolling(window).mean()/data.strategy_ret.rolling(window).std()
    return data

# Compute rolling volatility and store it in variable volatility
def rolling_volatility(data,window):    
    data['volatility'] = data.strategy_ret.rolling(window).std()
    return data