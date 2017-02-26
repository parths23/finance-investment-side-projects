"""python historical_analysis/scripts/data_ingestion.py --stock_symbols spy,gld"""

import argparse
import MySQLdb
import csv
from datetime import datetime


def parse_commandline():
    """Command line options."""
    parser = argparse.ArgumentParser(description='Send')
    parser.add_argument('--stock_symbols', action='store', required=True,
                        help="Symbols of stocks to ingest data into mysql")
    parser.add_argument('--password', action='store', required=True,
                        help="password for finances user")
    parser.add_argument('--db_name', action='store', default='finances',
                        help="Name of db")
    parser.add_argument('--user', action='store', default='finances',
                        help="db user")
    parser.add_argument('--host', action='store', default='localhost',
                        help="db user")
    return parser.parse_args()


def validate_and_convert_row(symbol, row):
    try:
        valid_row = {}
        valid_row['date'] = _string_to_date(row['Date'])
        valid_row['price'] = float(row['Close'])
        valid_row['symbol'] = symbol
        print valid_row['date']
        return valid_row
    except Exception as e:
        print e
        return False


def _string_to_date(date_string):
    """
    Convert a string to a python datetime object.
    Will attempt to match date format with commonly used string representations.
    :param date_string: string representation of date
    :rtype: string of date in "Y-m-d" format
    """
    if date_string == '':
        return ''
    formats = (
        '%d-%b-%Y', '%Y-%m-%d',
    )
    for fmt in formats:
        try:
            result = datetime.strptime(date_string, fmt)
            return result.strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError('Unknown date format: {0}'.format(date_string))


def main():
    args = parse_commandline()
    db = MySQLdb.connect(host=args.host, user=args.user, passwd=args.password, db=args.db_name)
    db.query("DROP TABLE IF EXISTS daily_prices")
    db.query(
        """CREATE TABLE IF NOT EXISTS daily_prices (symbol CHAR(20), price FLOAT(20), date_of_price DATE)""")
    stock_symbols = args.stock_symbols.split(',')
    for symbol in stock_symbols:
        csv_file_name = 'historical_analysis/data/' + symbol + '.csv'
        with open(csv_file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row = validate_and_convert_row(symbol, row)
                if row:
                    db.query("""INSERT INTO daily_prices (symbol,price,date_of_price) VALUES('{0}',{1},'{2}');""".format(
                        row['symbol'], row['price'], row['date']))


if __name__ == '__main__':
    main()
