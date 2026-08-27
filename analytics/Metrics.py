import numpy as np
import pandas as pd
from database.repository_price import RepoPrice

rpp = RepoPrice()

class Metrics:
    def log_return(self,symbols : list[str])-> pd.DataFrame:
        symbols = list(symbols)

        if len(symbols) < 2:
            raise ValueError("Give corr() at least two symbols")

        if len(symbols) != len(set(symbols)):
            raise ValueError("Symbols must not contain duplicates")

        price_col = []

        for symbol in symbols:
            df = rpp.get_price_all(symbol)
            if df is None or df.empty:
                raise ValueError(f"No price data found for {symbol}")
            prices = (
                df[["trading_date","close_price"]]
                .dropna()
                .sort_values("trading_date")
                .set_index("trading_date")["close_price"]
                .astype(float)
                .rename(symbol)
            )
            price_col.append(prices)
        close_prices = pd.concat(
            price_col,
            axis = 1,
            join = "inner"
        ).sort_index()

        if len(close_prices) < 3:
            raise ValueError("Not enough shared trading dates")
        if(close_prices <=0).any().any():
            raise ValueError("Close prices must be positive for log returns")
        log_R = np.log(close_prices/close_prices.shift(1))*100

        return log_R


    def corr(self,symbols : list[str]) -> pd.DataFrame:
        log_R = self.log_return(symbols)
        return log_R.corr(method ="pearson")


