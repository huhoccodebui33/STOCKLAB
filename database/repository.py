

from database.connection import getConnection


class Repository:
    def insert_stock(self,symbol, company_name,exchange):
        conn = getConnection()
        cur = conn.cursor()
        sql ="""
            INSERT INTO stocks(symbol, company_name, exchange)
            VALUES (%s,%s,%s)
            """
        cur.execute(sql,(symbol,company_name,exchange))
        conn.commit()
        cur.close()
        conn.close()

    def insert_price(self,stock_id, trading_date, open_price, high, low, close_price,volume):
        conn = getConnection()
        cur  = conn.cursor()
        sql = """ INSERT INTO daily_prices(stock_id,trading_date,open_price,high,low,close_price,volume) 
                VALUES (%s,%s,%s,%s,%s,%s,%s)
              """
        cur.execute(sql,(stock_id, trading_date, open_price, high, low, close_price,volume))
        conn.commit()
        cur.close()
        conn.close()

    def get_stockID(self,symbol):
        conn = getConnection()
        cur = conn.cursor()
        sql=""" SELECT id FROM stocks WHERE symbol = %s """
        cur.execute(sql,(symbol,))
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return row[0]
        
        