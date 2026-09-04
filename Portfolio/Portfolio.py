from datetime import date
from math import isfinite
from numbers import Real

from database.repository_price import RepoPrice
rpp = RepoPrice()

class Portfolio:
    def __init__(self, capital: float):
        if isinstance(capital, bool) or not isinstance(capital, Real):
            raise TypeError("capital must be a number")

        if not isfinite(float(capital)) or capital < 0:
            raise ValueError(
                "capital must be a finite, non-negative number"
            )
        self.initial_capital = capital
        self.balance = capital
        self.total_owned_stocks: dict[str, float] = {}
        self.trade_history: list[dict] = []
        self.total_short_stocks: dict[str, float] = {}

    def buy(self, symbol:str, quantity: float, trading_date:str):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        price = float(rpp.get_price_btw(symbol,start_date=trading_date,end_date=trading_date)["close_price"].iloc[0])
        cur_cost = price*quantity
        if cur_cost > self.balance:
            print("Balance is not enough")
            return None
        else: 
            old_quantity = self.total_owned_stocks.get(symbol, 0)
            new_quantity = old_quantity + quantity
            self.balance -= cur_cost
            self.total_owned_stocks[symbol] = new_quantity
            self.trade_history.append({
                    "symbol": symbol,
                    "quantity": quantity,
                    "asset_type": "stock",
                    "side": "BUY",
                    "trading_date": trading_date,
                    "price": price,
                    "cost": cur_cost
                })
    
    def sell(self, symbol:str, quantity: float, trading_date:str):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        close_price = rpp.get_price_btw(symbol,start_date=trading_date,end_date=trading_date)["close_price"].iloc[0]
        old_quantity = self.total_owned_stocks.get(symbol, 0)

        if quantity > old_quantity:
          print("Stock is not enough")
          return None
        else:
              cur_income = close_price*quantity
              self.balance += cur_income
              self.total_owned_stocks[symbol] -= quantity

              self.trade_history.append({
                    "symbol": symbol,
                    "quantity": quantity,
                    "asset_type": "stock",
                    "side": "SELL",
                    "trading_date": trading_date,
                    "price": close_price,
                    "income": cur_income

              })

        if self.total_owned_stocks[symbol] == 0:
            del self.total_owned_stocks[symbol]

    def get_portfolio_value(self, trading_date: str):
        long_value = 0.0
        short_value = 0.0

        # Giá trị cổ phiếu đang hold
        for symbol, quantity in self.total_owned_stocks.items():
            close_price = float(rpp.get_price_btw(
                symbol,
                start_date=trading_date,
                end_date=trading_date
            )["close_price"].iloc[0])

            long_value += close_price * quantity

        # Giá trị nghĩa vụ phải mua lại của SHORT
        for symbol, quantity in self.total_short_stocks.items():
            close_price = rpp.get_price_btw(
                symbol,
                start_date=trading_date,
                end_date=trading_date
            )["close_price"].iloc[0]

            short_value += close_price * quantity

        return self.balance + long_value - short_value

    def get_pnl(self, trading_date: str):
        current_value = self.get_portfolio_value(trading_date)
        return current_value - self.initial_capital

    def short(self, symbol: str, quantity: float, trading_date: str):
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        open_price = rpp.get_price_btw(
            symbol,
            start_date=trading_date,
            end_date=trading_date
        )["close_price"].iloc[0]

        income = open_price * quantity

        old_quantity = self.total_short_stocks.get(symbol, 0)
        new_quantity = old_quantity + quantity

        # Bán khống → nhận tiền
        self.balance += income

        self.total_short_stocks[symbol] = new_quantity

        self.trade_history.append({
            "symbol": symbol,
            "quantity": quantity,
            "asset_type": "stock",
            "side": "SHORT",
            "trading_date": trading_date,
            "price": open_price,
            "income": income
        })
    def cover(self, symbol: str, quantity: float, trading_date: str):
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        old_quantity = self.total_short_stocks.get(symbol, 0)

        if quantity > old_quantity:
            print("Short position is not enough")
            return None

        close_price = rpp.get_price_btw(
            symbol,
            start_date=trading_date,
            end_date=trading_date
        )["close_price"].iloc[0]

        cost = close_price * quantity

        # Mua lại để đóng short
        self.balance -= cost

        self.total_short_stocks[symbol] -= quantity

        self.trade_history.append({
            "symbol": symbol,
            "quantity": quantity,
            "asset_type": "stock",
            "side": "COVER",
            "trading_date": trading_date,
            "price": close_price,
            "cost": cost
        })

        if self.total_short_stocks[symbol] == 0:
            del self.total_short_stocks[symbol]