
from database.repository import Repository
from vnstock.ui import Market

mkt = Market()
repo = Repository()

df = mkt.equity("VIC").ohlcv(interval = "1D", count = 10)
repo.insert_stock("VIC","VINGROUP","HOSE")
id = repo.get_stockID("VIC")
for row in df.itertuples(index = False):
    repo.insert_price(
        id,
        row.time,
        row.open,
        row.high,
        row.low,
        row.close,
        row.volume
    )


# hôm nay đã viết cái repo, nhưng cái phần thêm giá đang hơi yếu, cũng như nên cho một số cái try và except