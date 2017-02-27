"""python analysis/scripts/data_ingestion.py --stock_symbols spy,gld"""

import argparse
import csv
from analysis.models.daily_price import DailyPrice
from analysis.models.db import db
from datetime import date, timedelta
from analysis.models.utils import prior_date


def parse_commandline():
    """Command line options."""
    parser = argparse.ArgumentParser(description='Send')
    parser.add_argument('--stock_symbols', action='store', required=True,
                        help="Symbols of stocks to ingest data into mysql")
    return parser.parse_args()


def main():
    args = parse_commandline()
    db.create_table(
        "daily_prices", "(id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY, symbol CHAR(20), price FLOAT(20), date DATE, previous_month_performance FLOAT(20))", drop_table=True)
    stock_symbols = args.stock_symbols.split(',')
    for symbol in stock_symbols:
        csv_file_name = 'analysis/data/' + symbol + '.csv'
        with open(csv_file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["Symbol"] = symbol
                DailyPrice(row)

    for symbol in stock_symbols:
        results = DailyPrice.fetch_all_for_symbol(symbol)
        for result in results:
            current_id = result[0]
            current_date = result[3]
            current_price = result[2]
            current_day = current_date.day
            previous_month_date = prior_date(current_date.isoformat(), days=30)
            if current_date.year >= 2005:
                prior_month_price = DailyPrice.get_historical(symbol, previous_month_date)
                percent_change = (current_price - prior_month_price) / prior_month_price * 100
                DailyPrice.update(current_id, 'previous_month_performance', percent_change)


if __name__ == '__main__':
    main()
