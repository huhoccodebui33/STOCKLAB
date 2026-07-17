from sqlalchemy import create_engine
import pandas as pd
from vnstock.ui import Market

# 1. Lấy dữ liệu FPT từ vnstock
mkt = Market()
FPT = mkt.equity("FPT").ohlcv(interval='1D', count=100)
df_FPT = pd.DataFrame(FPT)

# Thêm cột symbol để biết đây là dữ liệu của mã nào (vì vnstock bản mới có thể chỉ trả về giá)
df_FPT['symbol'] = 'FPT'

# 2. Tạo kết nối đến PostgreSQL (Docker) bằng SQLAlchemy
# Công thức: postgresql://[user]:[password]@[host]:[port]/[database]
engine = create_engine('postgresql://postgres:123456@localhost:5432/vnstock')

# 3. Một dòng duy nhất để đẩy toàn bộ DataFrame vào bảng 'daily_prices'
# if_exists='append': Nếu bảng chưa có thì tự động tạo, nếu có rồi thì chèn thêm vào cuối bảng
df_FPT.to_sql('daily_prices', engine, if_exists='append', index=False)

print("Đã lưu dữ liệu FPT vào PostgreSQL thành công!")