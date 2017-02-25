"""python historical_analysis.py --stock_symbols spy,gld --start_year 2005 --end_year 2006 --monthly_contribution 2000."""
import argparse
from yahoo_finance import Share


def parse_commandline():
    """Command line options."""
    parser = argparse.ArgumentParser(description='Send')
    parser.add_argument('--stock_symbols', action='store', required=True,
                        help="Symbols of stocks to analyze")
    parser.add_argument('--start_year', action='store', required=True,
                        help="Year to start analysis of rebalancing strategy")
    parser.add_argument('--end_year', action='store', required=True,
                        help="Year to stop analysis of rebalancing strategy")
    parser.add_argument('--monthly_contribution', action='store', required=True,
                        help="Initial Monthly contribution to account")
    return parser.parse_args()


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
        self._initiate_stock_dict(stock_symbols)

    def _initiate_stock_dict(self, stock_symbols):
        stock_symbols = stock_symbols.strip().split(',')
        for stock_symbol in stock_symbols:
            self._update_stock_price(stock_symbol)

    def _format_current_date(self):
        return "{0}-{1}-25".format(self.current_year, self.current_month)

    def _get_stock_price(self, stock_symbol):
        try:
            stock = Share(stock_symbol)
            price = stock.get_historical(
                self._format_current_date(), self._format_current_date())[0]['Open']
            return float(price)
        except:
            return self.stocks[stock_symbol]['price']

    def _update_stock_price(self, stock_symbol):
        price = self._get_stock_price(stock_symbol)
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
                    if rebalance and self.current_month % self.rebalance_interval == 0:
                        self._rebalance_portfolio()
        self._sell_stocks()

    def _rebalance_portfolio(self):
        """Method rebalances the portfolio to equal distribution based on a parameter time interval."""
        self._sell_stocks()
        self._buy_stocks()


class PortfolioManager():

    def __init__(self, args):
        self.portfolio_runs = []
        self.args = args
        self.rebalancing_intervals = [1, 2, 3, 4, 6, 12]

    def _run_portfolio(self, args, invest, rebalance):
        portfolio = Portfolio(
            args.interval, args.start_year, args.end_year, args.monthly_contribution, args.stock_symbols)
        portfolio.run(invest, rebalance)
        self.portfolio_runs.append(portfolio)
        print portfolio.cash_balance

    def manage_portfolio_runs(self):
    	self.args.interval = 0
        self._run_portfolio(self.args, invest=False, rebalance=False)
        for interval in self.rebalancing_intervals:
            self.args.interval = interval
            self._run_portfolio(self.args, invest=True, rebalance=False)
            self._run_portfolio(self.args, invest=True, rebalance=True)

        self._sort_portfolio_runs()
        import pdb
        pdb.set_trace()

    def _sort_portfolio_runs(self):
        self.portfolio_runs.sort(key=lambda x: x.cash_balance, reverse=True)


def main():
    args = parse_commandline()
    portfolio_manager = PortfolioManager(args)
    portfolio_manager.manage_portfolio_runs()


if __name__ == '__main__':
    main()
