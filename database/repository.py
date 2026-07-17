

from database.connection import get_connection


class PriceRepository:

    def __init__(self):

        # Tạo kết nối PostgreSQL
        self.conn = get_connection()

        # Cursor dùng để thực thi SQL
        self.cursor = self.conn.cursor()