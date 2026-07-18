

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import getConnection


class PriceRepository:

    def __init__(self):

        # Tạo kết nối PostgreSQL
        self.conn = getConnection()

        # Cursor dùng để thực thi SQL
        self.cursor = self.conn.cursor()