
import pandas as pd
from database.connection import getConnection


class Repository:
    def insert_stock(self,symbol, company_name,exchange):
        conn = None
        cur = None
        try:
            conn = getConnection()
            cur = conn.cursor()
            sql ="""
                INSERT INTO stocks(symbol, company_name, exchange)
                VALUES (%s,%s,%s)
                ON CONFLICT (symbol) DO NOTHING
                """
            cur.execute(sql,(symbol,company_name,exchange))
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            print(e)
        finally:
            if conn:
                conn.close()
            if cur:
                cur.close()

    def insert_price(self,stock_id, trading_date, open_price, high, low, close_price,volume):
        conn = None
        cur = None
        try:
            conn = getConnection()
            cur  = conn.cursor()
            sql = """ INSERT INTO daily_prices(stock_id,trading_date,open_price,high,low,close_price,volume) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (stock_id, trading_date) DO NOTHING
                """
            cur.execute(sql,(stock_id, trading_date, open_price, high, low, close_price,volume))
            conn.commit()
        except Exception as e: 
            if conn is not None:
                conn.rollback()
            print(e)
        finally:
            if conn:
                conn.close()
            if cur:
                cur.close()

    def get_stockID(self, symbol):
        conn = None
        cur = None
        try:
            conn = getConnection()
            cur = conn.cursor()
            sql = "SELECT id FROM stocks WHERE symbol = %s"
            cur.execute(sql, (symbol,))
            row = cur.fetchone()
            if row is None:
                return None
            return row[0]
        
        except Exception as e:
            print(e)
            return None
        
        finally:
            if cur:
                cur.close()

            if conn:
                conn.close()

    def get_ohlcv(self,symbol):
        conn = None
        try:
            conn = getConnection()
            sql ="""SELECT
                    dp.id,
                    dp.trading_date,
                    dp.open_price,
                    dp.high,
                    dp.low,
                    dp.close_price,
                    dp.volume
                    FROM daily_prices dp
                    JOIN stocks s ON dp.stock_id = s.id
                    WHERE s.symbol = %s
                    ORDER BY dp.trading_date
                     """      
            df = pd.read_sql(sql,conn,params=(symbol,)) 
            return df
        except Exception as e:
            print(e)
            return None
        finally:
            if conn:
                conn.close()
