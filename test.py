from database.repository_stock import RepoStock
from database.resporitory_price import RepoPrice
from vnstock.ui import Market
import pandas as pd

mkt = Market()
stock_data = RepoStock()
stock_price = RepoPrice()
df  = pd.DataFrame(mkt.equity("VIC").ohlcv(interval = "1D", count = 1000))
id = stock_data.get_stockID("VIC")
stock_price.insert_many_price(id,df)

