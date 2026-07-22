from ETL.Extract import Extract_by_date, Extract_by_limit
from database.repository_stock import RepoStock
from database.repository_price import RepoPrice
from ETL.Transform import Transform_price
stock_repo = RepoStock()
price_repo = RepoPrice()

class Pipeline:           
    def run(self,stocks,config):
        for data in stocks:
            if not stock_repo.exist_stock(symbol=data["symbol"]):
                stock_repo.insert_stock(data["symbol"], data["company_name"],data["exchange"])
                print(f'{data["symbol"]} is inserted into database')

            stock_id = stock_repo.get_stockID(data["symbol"])

            if config["mode"] == "limit":
                df = Extract_by_limit(data["symbol"],config["interval"], config["limit"])

            elif config["mode"] == "date":
                df = Extract_by_date(data["symbol"],config["interval"], config["start_date"],config["end_date"])

            else:
                raise ValueError("Invalid mode")
            df = Transform_price(df)
            price_repo.insert_many_price(stock_id,df)