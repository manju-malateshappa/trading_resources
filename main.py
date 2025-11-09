#!/usr/bin/env python3
"""
Investment Agent - Main CLI Interface

A comprehensive AI-powered investment analysis and portfolio management system
focused on identifying high-growth small/mid-cap stocks for 100-200% returns.
"""

import argparse
import sys
from pathlib import Path

# Add the project directory to path
sys.path.insert(0, str(Path(__file__).parent))

from investment_agent.agent import InvestmentAgent
from investment_agent.utils.logger import logger
from rich.console import Console
from rich.table import Table


console = Console()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Investment Agent - AI-Powered Investment Analysis & Portfolio Management"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan market for opportunities')
    scan_parser.add_argument(
        '--markets',
        nargs='+',
        default=['TSX', 'NASDAQ'],
        help='Markets to scan (default: TSX NASDAQ)'
    )

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a specific stock')
    analyze_parser.add_argument('symbol', help='Stock ticker symbol')

    # Recommend command
    recommend_parser = subparsers.add_parser('recommend', help='Get investment recommendations')
    recommend_parser.add_argument(
        '--focus',
        choices=['growth', 'value', 'breakout'],
        default='growth',
        help='Recommendation focus (default: growth)'
    )
    recommend_parser.add_argument(
        '--min-score',
        type=float,
        default=70.0,
        help='Minimum score (default: 70.0)'
    )

    # Evaluate buy command
    buy_parser = subparsers.add_parser('buy', help='Evaluate buying a stock')
    buy_parser.add_argument('symbol', help='Stock ticker symbol')
    buy_parser.add_argument(
        '--shares',
        type=int,
        help='Number of shares (optional, will auto-calculate)'
    )

    # Evaluate sell command
    sell_parser = subparsers.add_parser('sell', help='Evaluate selling a stock')
    sell_parser.add_argument('symbol', help='Stock ticker symbol')

    # Daily routine
    daily_parser = subparsers.add_parser('daily', help='Run daily routine')

    # Portfolio command
    portfolio_parser = subparsers.add_parser('portfolio', help='View portfolio summary')

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize agent
    console.print("[bold green]Initializing Investment Agent...[/bold green]")
    agent = InvestmentAgent()

    # Execute command
    if args.command == 'scan':
        console.print(f"\n[bold blue]Scanning markets: {', '.join(args.markets)}[/bold blue]")
        opportunities = agent.scan_market(markets=args.markets)

        if not opportunities.empty:
            display_opportunities_table(opportunities.head(20))
        else:
            console.print("[yellow]No opportunities found[/yellow]")

    elif args.command == 'analyze':
        console.print(f"\n[bold blue]Analyzing {args.symbol}[/bold blue]")
        analysis = agent.analyze_stock(args.symbol)

    elif args.command == 'recommend':
        console.print(f"\n[bold blue]Getting {args.focus} recommendations[/bold blue]")
        recommendations = agent.get_recommendations(
            min_score=args.min_score,
            focus=args.focus
        )

        if not recommendations.empty:
            display_opportunities_table(recommendations.head(15))
        else:
            console.print("[yellow]No recommendations found[/yellow]")

    elif args.command == 'buy':
        console.print(f"\n[bold blue]Evaluating BUY for {args.symbol}[/bold blue]")
        evaluation = agent.evaluate_buy(args.symbol, shares=args.shares)

        display_buy_evaluation(evaluation)

    elif args.command == 'sell':
        console.print(f"\n[bold blue]Evaluating SELL for {args.symbol}[/bold blue]")
        evaluation = agent.evaluate_sell(args.symbol)

        display_sell_evaluation(evaluation)

    elif args.command == 'daily':
        console.print("\n[bold blue]Running Daily Routine[/bold blue]")
        results = agent.daily_routine()

        # Display results
        if results['opportunities'] is not None and not results['opportunities'].empty:
            console.print("\n[bold green]Today's Top Opportunities:[/bold green]")
            display_opportunities_table(results['opportunities'].head(10))

        if results['position_alerts']:
            console.print("\n[bold yellow]Position Alerts:[/bold yellow]")
            for alert in results['position_alerts']:
                console.print(f"  • {alert['symbol']}: {alert['action']} - {', '.join(alert['reasons'])}")

    elif args.command == 'portfolio':
        display_portfolio_summary(agent)


def display_opportunities_table(df):
    """Display opportunities in a formatted table."""
    table = Table(title="Investment Opportunities", show_header=True, header_style="bold magenta")

    table.add_column("Symbol", style="cyan", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Score", justify="right", style="green")
    table.add_column("Signal", justify="center")
    table.add_column("2Y Return", justify="right", style="yellow")
    table.add_column("Risk", justify="center")
    table.add_column("Price", justify="right", style="blue")

    for _, row in df.iterrows():
        # Color code signal
        signal = row.get('recommendation', 'hold').upper()
        signal_color = 'green' if 'BUY' in signal else 'yellow' if 'HOLD' in signal else 'red'

        # Color code risk
        risk = row.get('risk_level', 'medium')
        risk_color = 'green' if risk == 'low' else 'yellow' if risk == 'medium' else 'red'

        table.add_row(
            str(row.get('symbol', '')),
            str(row.get('name', ''))[:30],
            f"{row.get('overall_score', 0):.1f}",
            f"[{signal_color}]{signal}[/{signal_color}]",
            f"{row.get('expected_return_2y', 0):.1%}",
            f"[{risk_color}]{risk.upper()}[/{risk_color}]",
            f"${row.get('current_price', 0):.2f}"
        )

    console.print(table)


def display_buy_evaluation(evaluation):
    """Display buy evaluation results."""
    action = evaluation.get('action', 'SKIP')
    color = 'green' if action == 'BUY' else 'yellow'

    console.print(f"\n[bold {color}]Action: {action}[/bold {color}]")

    if action == 'BUY':
        console.print(f"Symbol: {evaluation['symbol']}")
        console.print(f"Shares: {evaluation['shares']}")
        console.print(f"Price: ${evaluation['current_price']:.2f}")
        console.print(f"Total Cost: ${evaluation['total_cost']:,.2f}")
        console.print(f"Overall Score: {evaluation['overall_score']:.1f}/100")
        console.print(f"Risk Level: {evaluation['risk_level']}")
        console.print(f"Expected 2Y Return: {evaluation['expected_return_2y']:.1%}")
        console.print(f"\nStop Loss: ${evaluation['stop_loss']:.2f}")

        console.print("\nTake Profit Levels:")
        for level, data in evaluation['take_profit_levels'].items():
            console.print(f"  {level}: ${data['price']:.2f} (sell {data['sell_percentage']:.0%})")
    else:
        console.print(f"Reason: {evaluation.get('reason', 'Unknown')}")


def display_sell_evaluation(evaluation):
    """Display sell evaluation results."""
    action = evaluation.get('action', 'SKIP')
    color = 'red' if action == 'SELL' else 'green'

    console.print(f"\n[bold {color}]Action: {action}[/bold {color}]")

    if action != 'SKIP':
        console.print(f"Symbol: {evaluation['symbol']}")
        console.print(f"Shares: {evaluation['shares']}")
        console.print(f"Entry Price: ${evaluation['entry_price']:.2f}")
        console.print(f"Current Price: ${evaluation['current_price']:.2f}")
        console.print(f"Return: {evaluation['return']:.2%}")
        console.print(f"P/L: ${evaluation['profit_loss']:,.2f}")

        if evaluation.get('reasons'):
            console.print("\nReasons:")
            for reason in evaluation['reasons']:
                console.print(f"  • {reason}")
    else:
        console.print(f"Reason: {evaluation.get('reason', 'Unknown')}")


def display_portfolio_summary(agent):
    """Display portfolio summary."""
    portfolio = agent.portfolio

    console.print("\n[bold blue]Portfolio Summary[/bold blue]")
    console.print(f"Name: {portfolio.name}")
    console.print(f"Cash: ${portfolio.cash:,.2f}")
    console.print(f"Positions: {len(portfolio.positions)}")

    if portfolio.positions:
        table = Table(title="Current Positions", show_header=True, header_style="bold magenta")

        table.add_column("Symbol", style="cyan")
        table.add_column("Shares", justify="right")
        table.add_column("Avg Price", justify="right", style="blue")
        table.add_column("Cost Basis", justify="right")
        table.add_column("Entry Date", style="white")

        for symbol, position in portfolio.positions.items():
            table.add_row(
                symbol,
                f"{position.shares:.0f}",
                f"${position.average_price:.2f}",
                f"${position.cost_basis:,.2f}",
                position.entry_date.strftime('%Y-%m-%d')
            )

        console.print(table)


if __name__ == '__main__':
    main()
