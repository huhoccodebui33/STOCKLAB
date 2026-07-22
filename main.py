from ETL.pipeline import Pipeline
from stock_config import STOCKS, CONFIG


def main():

    pipeline = Pipeline()

    pipeline.run(
        stocks=STOCKS,
        config=CONFIG
    )


if __name__ == "__main__":
    main()