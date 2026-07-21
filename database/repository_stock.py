
import pandas as pd
from database.connection import getConnection


class RepoStock:
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
    def get_stock(self,symbol):
        conn = None
        cur = None
        row = None
        try:
            conn = getConnection()
            cur = conn.cursor()
            sql = """SELECT id, symbol, company_name, exchange FROM stocks WHERE symbol = %s"""
            cur.execute(sql,(symbol,))
            row = cur.fetchone()
            if row is not None:
                return row
            else:
                return None
        except Exception as e:
            print(e)
            return None
        finally:
            cur.close()
            conn.close()

    def get_all_stock(self):
        conn = None
        cur = None
        row = None
        try:
            conn = getConnection()
            cur = conn.cursor()
            sql = """SELECT * FROM stocks"""
            cur.execute(sql)
            row = cur.fetchall()
            if row is not None:
                return row
            else:
                return None
        except Exception as e:
            print(e)
            return None
        finally:
            cur.close()
            conn.close()

    def exist_stock(self,symbol):
        conn = None
        cur = None
        row = None
        try:
            conn = getConnection()
            cur  = conn.cursor()
            sql = "SELECT id FROM stocks WHERE symbol = %s"
            cur.execute(sql, (symbol,))
            row = cur.fetchone()
            if row:
                return True
            else:
                return False
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def count_stock(self):
        conn = None
        cur = None
        row = None
        try: 
            conn = getConnection()
            cur = conn.cursor()
            sql ="""SELECT COUNT( *) FROM stocks"""
            cur.execute(sql)
            row = cur.fetchone()
            if row:
                return row[0]
            else: 
                return None
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()
    

