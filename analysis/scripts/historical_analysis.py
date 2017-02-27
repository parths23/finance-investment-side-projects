"""python analysis/scripts/historical_analysis.py --stock_symbols spy,gld --start_year 2007 --end_year 2012 --monthly_contribution 2000."""
import argparse
from analysis.models.portfolio_analyzer import PortfolioAnalyzer


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


def main():
    args = parse_commandline()
    portfolio_manager = PortfolioAnalyzer(args)
    portfolio_manager.run_portfolio_models()


if __name__ == '__main__':
    main()
