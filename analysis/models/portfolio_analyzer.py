"""Portfolio Manager."""
from portfolio import Portfolio
import csv


class PortfolioAnalyzer():

    def __init__(self, args):
        self.portfolio_runs = []
        self.args = args

    def _run_portfolio(self, args, invest, rebalance):
        portfolio = Portfolio(args.start_year, args.end_year, args.monthly_contribution, args.stock_symbols)
        portfolio.run(invest, rebalance)
        self.portfolio_runs.append(portfolio)
        self.write_results_to_csv()

    def run_portfolio_models(self):
        self._run_portfolio(self.args, invest=False, rebalance=False)
        original_stocks = self.args.stock_symbols
        self.args.stock_symbols = 'spy'
        self._run_portfolio(self.args, invest=True, rebalance=False)
        self.args.stock_symbols = original_stocks
        self._run_portfolio(self.args, invest=True, rebalance=False)
        self._run_portfolio(self.args, invest=True, rebalance=True)

    def write_results_to_csv(self):
        self._sort_portfolio_runs()
        csv_file_name = 'analysis/results/' + self.args.start_year + '_' + \
            self.args.end_year + '_results_' + self.args.stock_symbols + '.csv'
        with open(csv_file_name, 'w') as csvfile:
            fieldnames = ['start_year', 'end_year', 'end_balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for portfolio in self.portfolio_runs:
                writer.writerow({'start_year': portfolio.start_year, 'end_year': portfolio.end_year,
                                 'end_balance': portfolio.cash_balance})

    def _sort_portfolio_runs(self):
        self.portfolio_runs.sort(key=lambda x: x.cash_balance, reverse=True)
