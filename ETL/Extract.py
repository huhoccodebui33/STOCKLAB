from vnstock.ui import Market
import pandas as pd

mkt = Market()

def Extract_by_date(symbol:str, interval:str,start_date:str, end_date:str) -> pd.DataFrame:
    try:
        df = mkt.equity(symbol).ohlcv(interval = interval,start = start_date, end = end_date)
        return df
    except Exception as e:
        print(e)
        return None

def Extract_by_limit(symbol:str, interval:str, limit:int) -> pd.DataFrame:
    try:
        df = mkt.equity(symbol).ohlcv(interval = interval, count = limit) 
        return df
    except Exception as e:
        print(e)
        return None