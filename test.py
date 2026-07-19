from database.repository import Repository
import pandas as pd

repo = Repository()
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
df_VIC = repo.get_ohlcv("VIC")
print(df_VIC.to_string(index= False))