from database.connection import getConnection
from psycopg2.extras import execute_values
import pandas as pd

class RepoPrice:
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

    def get_price_all(self,symbol):
        conn = None
        try:
            conn = getConnection()
            sql ="""SELECT
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

    def get_price_btw(self,symbol,start_date: str, end_date:str): #year-month-date (2999-02-02)
        conn = None
        try:
            conn = getConnection()
            sql = """SELECT
                    dp.trading_date,
                    dp.open_price,
                    dp.high,
                    dp.low,
                    dp.close_price,
                    dp.volume
                    FROM daily_prices dp
                    JOIN stocks s ON dp.stock_id = s.id
                    WHERE s.symbol = %s
                        AND dp.trading_date BETWEEN %s AND %s
                    ORDER BY dp.trading_date
                     """
            df = pd.read_sql(sql,conn, params=(symbol,start_date,end_date))
            return df
        except Exception as e:
            print(e)
            return None
        finally:
            if conn:
                conn.close()

    def get_price_limit(self, symbol, limit):
        conn = None
        try:
            conn = getConnection()
            sql ="""SELECT
                    dp.trading_date,
                    dp.open_price,
                    dp.high,
                    dp.low,
                    dp.close_price,
                    dp.volume
                    FROM daily_prices dp
                    JOIN stocks s ON dp.stock_id = s.id
                    WHERE s.symbol = %s
                    ORDER BY dp.trading_date DESC
                    LIMIT %s
                     """      
            df = pd.read_sql(sql,conn,params=(symbol,limit)) 
            return df
        except Exception as e:
            print(e)
            return None
        finally:
            if conn:
                conn.close()

    def insert_many_price(self,stock_id,df):
        conn = None
        cur = None
        try:
            conn = getConnection()
            cur = conn.cursor()
            sql =""" INSERT INTO daily_prices
            (
                stock_id,
                trading_date,
                open_price,
                high,
                low,
                close_price,
                volume
            )
            VALUES %s
            ON CONFLICT (stock_id, trading_date)
            DO NOTHING"""
            records = (
                (
                    stock_id,
                    row.time,
                    row.open,
                    row.high,
                    row.low,
                    row.close,
                    row.volume
                )
                for row in df.itertuples(index=False)
            )
            execute_values(cur, sql, records)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
