
import numpy as np


def sma_crossover(data, short_lookback, long_lookback):
    data['sma_short'] = data.Close.rolling(short_lookback).mean()
    data['sma_long'] = data.Close.rolling(long_lookback).mean()
    data['sma_signal'] = np.where(data.sma_short > data.sma_long, 1, -1)    
    return data

