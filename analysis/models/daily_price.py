from analysis.models.db import db
from utils import _string_to_date


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
        query = """INSERT INTO daily_prices (symbol,price,date_of_price) VALUES('{0}',{1},'{2}');""".format(
                self.symbol, self.price, self.date)
        return query

    def _validate_and_insert(self):
        self._validate_and_transform()
        if self.valid:
			query = self._create_sql_insert_query()
			db.query(query)
			print self.date
