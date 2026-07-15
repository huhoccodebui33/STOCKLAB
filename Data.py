from vnstock.ui import Market
import pandas as pd


mkt = Market()

FPT = mkt.equity("FPT").ohlcv(interval = '1D', count = 100)
df_FPT = pd.DataFrame(FPT)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
 
print(df_FPT)