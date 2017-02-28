"""Portfolio Manager."""
from portfolio import Portfolio
import csv


class PortfolioAnalyzer():

    def __init__(self, args):
        self.portfolio_runs = []
        self.args = args
        self.conditions = {}

    def _run_portfolio(self):
        portfolio = Portfolio(self.args, self.conditions)
        portfolio.run()
        self.portfolio_runs.append(portfolio)
        self.write_results_to_csv()

    def run_portfolio_models(self):
        # Mock run with no investment
        self.conditions['invest'] = False
        self.conditions['rebalance'] = False
        self.conditions['performance_period'] = 0
        self.conditions['performance_threshold'] = 0
        self.conditions['rebalance_ratio'] = 0
        self._run_portfolio()

        # Mock run with just s and p index
        original_stocks = self.args.stock_symbols
        self.args.stock_symbols = "spy"
        self.conditions['invest'] = True
        self._run_portfolio()
        self.args.stock_symbols = original_stocks

        # Mock run with just gold index
        original_stocks = self.args.stock_symbols
        self.args.stock_symbols = "gld"
        self.conditions['invest'] = True
        self._run_portfolio()
        self.args.stock_symbols = original_stocks

        # Mock run with equal split among all stocks and no rebalance
        self._run_portfolio()

        # Mock runs with different performance_period, performance_threshold, and rebalance_ratio
        self.conditions['rebalance'] = True
        performance_period_list = range(25, 36)
        performance_threshold_list = range(-20, -9)
        rebalance_ratio_list = [0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25]
        for x in performance_period_list:
            for y in performance_threshold_list:
                for z in rebalance_ratio_list:
                    self.conditions['performance_period'] = x
                    self.conditions['performance_threshold'] = float(y)
                    self.conditions['rebalance_ratio'] = z
                    self._run_portfolio()


# performance_period, performance_percentage, rebalance_ratio, profit

    def write_results_to_csv(self):
        self._sort_portfolio_runs()
        csv_file_name = 'analysis/results/' + self.args.start_year + '_' + \
            self.args.end_year + '_results' + '.csv'
        with open(csv_file_name, 'w') as csvfile:
            fieldnames = ['start_year', 'end_year', 'stock_symbols',
                          'invest', 'rebalance', 'performance_period', 'performance_threshold',
                          'rebalance_ratio', 'end_balance', ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for portfolio in self.portfolio_runs:
                writer.writerow({'start_year': portfolio.start_year,
                                 'end_year': portfolio.end_year,
                                 'stock_symbols': portfolio.stock_list,
                                 'invest': portfolio.invest,
                                 'rebalance': portfolio.rebalance,
                                 'performance_period': portfolio.performance_period,
                                 'performance_threshold': portfolio.performance_threshold,
                                 'rebalance_ratio': portfolio.rebalance_ratio,
                                 'end_balance': portfolio.cash_balance
                                 })

    def _sort_portfolio_runs(self):
        self.portfolio_runs.sort(key=lambda x: x.cash_balance, reverse=True)
