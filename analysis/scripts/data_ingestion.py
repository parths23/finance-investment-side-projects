"""python analysis/scripts/data_ingestion.py --stock_symbols spy,gld"""

import argparse
import csv
from analysis.models.daily_price import DailyPrice
from analysis.models.db import db


def parse_commandline():
    """Command line options."""
    parser = argparse.ArgumentParser(description='Send')
    parser.add_argument('--stock_symbols', action='store', required=True,
                        help="Symbols of stocks to ingest data into mysql")
    return parser.parse_args()


def main():
    args = parse_commandline()
    db.create_table(
        "daily_prices", "(symbol CHAR(20), price FLOAT(20), date_of_price DATE)", drop_table=True)
    stock_symbols = args.stock_symbols.split(',')
    for symbol in stock_symbols:
        csv_file_name = 'analysis/data/' + symbol + '.csv'
        with open(csv_file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["Symbol"] = symbol
                DailyPrice(row)


if __name__ == '__main__':
    main()
