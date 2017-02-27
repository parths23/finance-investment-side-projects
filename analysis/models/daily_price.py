from analysis.models.db import db
from utils import _string_to_date, prior_date


class DailyPrice():

    def __init__(self, args):
        self.date = args["Date"]
        self.price = args["Close"]
        self.symbol = args["Symbol"]
        self.valid = False
        self._validate_and_insert()

    def _validate_and_transform(self):
        self.date = _string_to_date(self.date)
        self.price = float(self.price)
        self.valid = True

    def _create_sql_insert_query(self):
        query = """INSERT INTO daily_prices (symbol,price,date) VALUES('{0}',{1},'{2}');""".format(
                self.symbol, self.price, self.date)
        return query

    @classmethod
    def update(self, id_key, column, value):
        query = """UPDATE daily_prices SET {0} = {1} WHERE id = {2}""".format(
            column, value, id_key)
        db.query(query)

    def _validate_and_insert(self):
        self._validate_and_transform()
        if self.valid:
            query = self._create_sql_insert_query()
            db.query(query)

    @classmethod
    def get_historical(cls, stock_symbol, date, retry=True):
        query = """SELECT price from daily_prices where date = '{0}' and symbol = '{1}';""".format(
            date, stock_symbol)
        prices = db.query(query)
        if not len(prices) and retry:
            new_date = prior_date(date, days=1)
            price = cls.get_historical(stock_symbol, new_date)
            return price
        else:
            return prices[0][0]

    @classmethod
    def fetch_all_for_symbol(cls, stock_symbol):
        query = """SELECT * from daily_prices where symbol='{0}'""".format(stock_symbol)
        return db.query(query)

    @classmethod
    def create_table(cls):
        db.create_table(
            "daily_prices", "(id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY, symbol CHAR(20), price FLOAT(20), date DATE)", drop_table=True)
