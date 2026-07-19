"""
migrate.py
----------------------------

Đọc file schema.sql và thực thi toàn bộ câu lệnh SQL.

Chỉ cần chạy file này một lần sau khi tạo database
hoặc mỗi khi thay đổi schema.
"""

from database.connection import getConnection


def migrate():

    # Kết nối PostgreSQL
    conn = getConnection()

    # Cursor dùng để gửi lệnh SQL
    cursor = conn.cursor()

    # Đọc toàn bộ file schema.sql
    with open("database/schema.sql", "r", encoding="utf-8") as file:
        sql = file.read()

    # Thực thi SQL
    cursor.execute(sql)

    # Lưu thay đổi
    conn.commit()

    print("✅ Database migrated successfully.")

    # Giải phóng tài nguyên
    cursor.close()
    conn.close()


if __name__ == "__main__":
    migrate()