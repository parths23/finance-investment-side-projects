from analysis.models.daily_price import DailyPrice

"""Portfolio Class."""


class Portfolio():

    """Portfolio class that represents a single run of a portfolio strategy over a certain time period."""

    def __init__(self, rebalance_interval, start_year, end_year, monthly_contribution, stock_symbols):
        self.cash_balance = 0.0
        self.rebalance_interval = int(rebalance_interval)
        self.start_year = int(start_year)
        self.end_year = int(end_year)
        self.initial_monthly_contribution = float(monthly_contribution)
        self.current_month = 1
        self.current_year = self.start_year
        self.stocks = {}
        self.stock_list = stock_symbols
        self._initiate_stock_dict(stock_symbols)

    def _initiate_stock_dict(self, stock_symbols):
        stock_symbols = stock_symbols.strip().split(',')
        for stock_symbol in stock_symbols:
            self._update_stock_price(stock_symbol)

    def _format_current_date(self):
        return "{0}-{1}-28".format(self.current_year, self.current_month)

    def _update_stock_price(self, stock_symbol):
        price = DailyPrice.get_historical(
            stock_symbol, self._format_current_date())
        if self.stocks.get(stock_symbol):
            self.stocks[stock_symbol]['price'] = price
            return price
        else:
            self.stocks[stock_symbol] = {'quantity': 0.0, 'price': price}
            return price

    def _purchase_stock(self, stock_symbol, cash_amount):
        price = self._update_stock_price(stock_symbol)
        stock_quantity = cash_amount / price
        self.stocks[stock_symbol]['quantity'] = self.stocks[
            stock_symbol]['quantity'] + stock_quantity
        purchase_cost = stock_quantity * price
        self.cash_balance -= purchase_cost

    def _sell_stock(self, stock_symbol):
        price = self.stocks[stock_symbol]['price']
        quantity = self.stocks[stock_symbol]['quantity']
        cash_back = price * quantity
        self.cash_balance += cash_back
        self.stocks[stock_symbol]['quantity'] = 0

    def _buy_stocks(self):
        stock_symbol_list = self.stocks.keys()
        number_of_stocks = float(len(stock_symbol_list))
        cash_per_stock = self.cash_balance / number_of_stocks
        for stock_symbol in stock_symbol_list:
            self._purchase_stock(stock_symbol, cash_per_stock)

    def _transfer_cash(self):
        multiplicative_factor = (self.current_year - self.start_year) * 250
        amount_saved = self.initial_monthly_contribution + float(multiplicative_factor)
        self.cash_balance += amount_saved

    def _sell_stocks(self):
        stock_symbol_list = self.stocks.keys()
        for stock_symbol in stock_symbol_list:
            self._sell_stock(stock_symbol)

    def run(self, invest, rebalance):
        """Method runs the portfolio from the January of start year to December of end year."""
        years = range(self.start_year, self.end_year + 1)
        for year in years:
            self.current_year = year
            for month in range(1, 13):
                self.current_month = month
                self._transfer_cash()
                if invest:
                    self._buy_stocks()
                    if rebalance:
                        self._rebalance_portfolio_general_interval_strategy()

        self._sell_stocks()

    def _rebalance_portfolio_general_interval_strategy(self):
        """Method rebalances the portfolio to equal distribution based on a parameter time interval."""
        if self.current_month % self.rebalance_interval == 0:
            self._sell_stocks()
            self._buy_stocks()
