"""Portfolio Manager."""
from portfolio import Portfolio
import csv


class PortfolioAnalyzer():

    def __init__(self, args):
        self.portfolio_runs = []
        self.args = args
        self.rebalancing_intervals = [1, 2, 3, 4, 6, 12]

    def _run_portfolio(self, args, invest, rebalance):
        portfolio = Portfolio(
            args.interval, args.start_year, args.end_year, args.monthly_contribution, args.stock_symbols)
        portfolio.run(invest, rebalance)
        self.portfolio_runs.append(portfolio)

    def run_portfolio_models(self):
        self.args.interval = 2
        self._run_portfolio(self.args, invest=True, rebalance=False)
        self.args.interval = 3
        self._run_portfolio(self.args, invest=True, rebalance=True)
        self.args.interval = 0
        self._run_portfolio(self.args, invest=False, rebalance=False)
        self.args.interval = 1
        original_stocks = self.args.stock_symbols
        self.args.stock_symbols = 'spy'
        self._run_portfolio(self.args, invest=True, rebalance=False)
        self.args.stock_symbols = original_stocks
        self._sort_portfolio_runs()

    def write_results_to_csv(self):
        csv_file_name = 'analysis/results/' + self.args.start_year + '_' + \
            self.args.end_year + '_results_' + self.args.stock_symbols + '.csv'
        with open(csv_file_name, 'w') as csvfile:
            fieldnames = ['start_year', 'end_year', 'rebalance_interval', 'end_balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for portfolio in self.portfolio_runs:
                writer.writerow({'start_year': portfolio.start_year, 'end_year': portfolio.end_year,
                                 'rebalance_interval': portfolio.rebalance_interval, 'end_balance': portfolio.cash_balance})

    def _sort_portfolio_runs(self):
        self.portfolio_runs.sort(key=lambda x: x.cash_balance, reverse=True)
