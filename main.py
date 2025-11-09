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
from investment_agent.utils import HelpSystem, favorites_manager
from investment_agent.data import company_db
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

    # AI companies command
    ai_parser = subparsers.add_parser('ai', help='Scan AI companies')
    ai_parser.add_argument(
        '--market',
        choices=['USA', 'CANADA', 'INDIA', 'ALL'],
        default='ALL',
        help='Market to scan (default: ALL)'
    )
    ai_parser.add_argument(
        '--min-score',
        type=float,
        default=65.0,
        help='Minimum score (default: 65.0)'
    )

    # Sector screening command
    sector_parser = subparsers.add_parser('sector', help='Scan specific sector')
    sector_parser.add_argument(
        'sector_name',
        help='Sector name (e.g., Fintech, "Cloud Computing", "EV & Clean Energy")'
    )
    sector_parser.add_argument(
        '--market',
        choices=['USA', 'CANADA', 'INDIA', 'ALL'],
        default='ALL',
        help='Market to scan (default: ALL)'
    )
    sector_parser.add_argument(
        '--min-score',
        type=float,
        default=65.0,
        help='Minimum score (default: 65.0)'
    )

    # Market-specific commands
    india_parser = subparsers.add_parser('india', help='Scan Indian market (NSE)')
    india_parser.add_argument(
        '--min-score',
        type=float,
        default=65.0,
        help='Minimum score (default: 65.0)'
    )

    canada_parser = subparsers.add_parser('canada', help='Scan Canadian market (TSX)')
    canada_parser.add_argument(
        '--min-score',
        type=float,
        default=65.0,
        help='Minimum score (default: 65.0)'
    )

    us_parser = subparsers.add_parser('us', help='Scan US market (NASDAQ, NYSE)')
    us_parser.add_argument(
        '--min-score',
        type=float,
        default=65.0,
        help='Minimum score (default: 65.0)'
    )

    # Help commands
    help_parser = subparsers.add_parser('help', help='Show help information')
    help_parser.add_argument('topic', nargs='?', help='Specific command to get help on')

    quick_parser = subparsers.add_parser('quick', help='Quick start guide')
    version_parser = subparsers.add_parser('version', help='Show version information')

    # Quick info commands
    info_parser = subparsers.add_parser('info', help='Quick stock information')
    info_parser.add_argument('symbol', help='Stock ticker symbol')

    score_parser = subparsers.add_parser('score', help='Show stock score breakdown')
    score_parser.add_argument('symbol', help='Stock ticker symbol')

    # Top stocks command
    top_parser = subparsers.add_parser('top', help='Show top N opportunities')
    top_parser.add_argument('count', type=int, default=10, nargs='?', help='Number of stocks (default: 10)')
    top_parser.add_argument('--market', choices=['USA', 'CANADA', 'INDIA'], help='Filter by market')

    # Favorites management
    fav_parser = subparsers.add_parser('fav', help='Manage favorite stocks')
    fav_subparsers = fav_parser.add_subparsers(dest='fav_command', help='Favorites commands')

    fav_add_parser = fav_subparsers.add_parser('add', help='Add stock to favorites')
    fav_add_parser.add_argument('symbol', help='Stock ticker symbol')
    fav_add_parser.add_argument('category', nargs='?', default='general', help='Category (default: general)')

    fav_remove_parser = fav_subparsers.add_parser('remove', help='Remove stock from favorites')
    fav_remove_parser.add_argument('symbol', help='Stock ticker symbol')

    fav_show_parser = fav_subparsers.add_parser('show', help='Show favorites')
    fav_show_parser.add_argument('category', nargs='?', help='Category filter (optional)')

    fav_categories_parser = fav_subparsers.add_parser('categories', help='List all categories')

    fav_scan_parser = fav_subparsers.add_parser('scan', help='Scan all favorites for signals')

    fav_export_parser = fav_subparsers.add_parser('export', help='Export favorites to file')
    fav_export_parser.add_argument('filepath', help='Output file path')

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        HelpSystem.show_all()
        return

    # Handle help commands without initializing agent
    if args.command == 'help':
        if args.topic:
            HelpSystem.show_command_help(args.topic)
        else:
            HelpSystem.show_all()
        return

    if args.command == 'quick':
        HelpSystem.show_quick_start()
        return

    if args.command == 'version':
        HelpSystem.show_version()
        return

    # Initialize agent for commands that need it
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

    elif args.command == 'ai':
        market = args.market if args.market != 'ALL' else None
        console.print(f"\n[bold blue]Scanning AI Companies - Market: {args.market}[/bold blue]")
        ai_companies = agent.stock_screener.screen_ai_companies(
            market=market,
            min_score=args.min_score
        )

        if not ai_companies.empty:
            display_opportunities_table(ai_companies.head(20))
        else:
            console.print("[yellow]No AI companies found meeting criteria[/yellow]")

    elif args.command == 'sector':
        market = args.market if args.market != 'ALL' else None
        console.print(f"\n[bold blue]Scanning {args.sector_name} - Market: {args.market}[/bold blue]")
        sector_companies = agent.stock_screener.screen_sector(
            sector=args.sector_name,
            market=market,
            min_score=args.min_score
        )

        if not sector_companies.empty:
            display_opportunities_table(sector_companies.head(20))
        else:
            console.print(f"[yellow]No companies found in {args.sector_name}[/yellow]")

    elif args.command == 'india':
        console.print("\n[bold blue]Scanning Indian Market (NSE)[/bold blue]")
        indian_stocks = agent.stock_screener.screen_indian_market(
            min_score=args.min_score
        )

        if not indian_stocks.empty:
            display_opportunities_table(indian_stocks.head(20))
        else:
            console.print("[yellow]No opportunities found in Indian market[/yellow]")

    elif args.command == 'canada':
        console.print("\n[bold blue]Scanning Canadian Market (TSX)[/bold blue]")
        canadian_stocks = agent.stock_screener.screen_canadian_market(
            min_score=args.min_score
        )

        if not canadian_stocks.empty:
            display_opportunities_table(canadian_stocks.head(20))
        else:
            console.print("[yellow]No opportunities found in Canadian market[/yellow]")

    elif args.command == 'us':
        console.print("\n[bold blue]Scanning US Market (NASDAQ, NYSE)[/bold blue]")
        us_stocks = agent.stock_screener.screen_us_market(
            min_score=args.min_score
        )

        if not us_stocks.empty:
            display_opportunities_table(us_stocks.head(20))
        else:
            console.print("[yellow]No opportunities found in US market[/yellow]")

    elif args.command == 'info':
        display_quick_info(agent, args.symbol)

    elif args.command == 'score':
        display_score_breakdown(agent, args.symbol)

    elif args.command == 'top':
        console.print(f"\n[bold blue]Top {args.count} Opportunities[/bold blue]")
        if args.market:
            screener_methods = {
                'USA': agent.stock_screener.screen_us_market,
                'CANADA': agent.stock_screener.screen_canadian_market,
                'INDIA': agent.stock_screener.screen_indian_market,
            }
            opportunities = screener_methods[args.market]()
        else:
            opportunities = agent.scan_market()

        if not opportunities.empty:
            display_opportunities_table(opportunities.head(args.count))
        else:
            console.print("[yellow]No opportunities found[/yellow]")

    elif args.command == 'fav':
        handle_favorites_command(agent, args)


def handle_favorites_command(agent, args):
    """Handle favorites management commands."""
    if not args.fav_command:
        # Show all favorites
        favorites = favorites_manager.get_all()
        if favorites:
            display_favorites(favorites)
        else:
            console.print("[yellow]No favorites yet. Add some with: fav add <ticker>[/yellow]")
        return

    if args.fav_command == 'add':
        # Get company info
        info = company_db.get_company_info(args.symbol)
        name = info.get('name', args.symbol)

        if favorites_manager.add(args.symbol, category=args.category, name=name):
            console.print(f"[green]✓[/green] Added {args.symbol} to favorites (category: {args.category})")
        else:
            console.print(f"[yellow]{args.symbol} already in favorites[/yellow]")

    elif args.fav_command == 'remove':
        if favorites_manager.remove(args.symbol):
            console.print(f"[green]✓[/green] Removed {args.symbol} from favorites")
        else:
            console.print(f"[yellow]{args.symbol} not found in favorites[/yellow]")

    elif args.fav_command == 'show':
        favorites = favorites_manager.get_all(category=args.category)
        if favorites:
            category_name = args.category if args.category else "All"
            console.print(f"\n[bold cyan]Favorites - {category_name}[/bold cyan]\n")
            display_favorites(favorites)
        else:
            console.print(f"[yellow]No favorites in category: {args.category}[/yellow]")

    elif args.fav_command == 'categories':
        categories = favorites_manager.get_categories()
        display_categories(categories)

    elif args.fav_command == 'scan':
        console.print("\n[bold blue]Scanning Favorites for Signals...[/bold blue]\n")
        symbols = favorites_manager.get_symbols()

        if not symbols:
            console.print("[yellow]No favorites to scan[/yellow]")
            return

        results = []
        for symbol in symbols:
            try:
                console.print(f"Analyzing {symbol}...")
                evaluation = agent.evaluate_buy(symbol)
                if evaluation.get('action') == 'BUY':
                    results.append(evaluation)
            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {str(e)}")

        if results:
            console.print(f"\n[bold green]Found {len(results)} BUY signals in favorites:[/bold green]\n")
            for result in results:
                console.print(f"  • {result['symbol']}: Score={result['overall_score']:.1f}")
        else:
            console.print("[yellow]No buy signals found in favorites[/yellow]")

    elif args.fav_command == 'export':
        if args.filepath.endswith('.json'):
            favorites_manager.export_to_json(args.filepath)
        else:
            favorites_manager.export_to_csv(args.filepath)
        console.print(f"[green]✓[/green] Exported favorites to {args.filepath}")


def display_quick_info(agent, symbol):
    """Display quick stock information."""
    fundamentals = agent.data_fetcher.get_fundamental_data(symbol)

    if not fundamentals:
        console.print(f"[red]Could not fetch data for {symbol}[/red]")
        return

    console.print(f"\n[bold cyan]{fundamentals.get('name', symbol)}[/bold cyan]")
    console.print(f"[dim]{symbol}  |  {fundamentals.get('sector', 'N/A')}[/dim]\n")

    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="yellow")
    table.add_column("Value", style="white")

    table.add_row("Current Price", f"${fundamentals.get('current_price', 0):.2f}")
    table.add_row("Market Cap", f"${fundamentals.get('market_cap', 0):,.0f}")
    table.add_row("P/E Ratio", f"{fundamentals.get('pe_ratio', 0):.2f}" if fundamentals.get('pe_ratio') else "N/A")
    table.add_row("Revenue Growth", f"{fundamentals.get('revenue_growth', 0):.1%}" if fundamentals.get('revenue_growth') else "N/A")
    table.add_row("Profit Margin", f"{fundamentals.get('profit_margin', 0):.1%}" if fundamentals.get('profit_margin') else "N/A")

    console.print(table)
    console.print()


def display_score_breakdown(agent, symbol):
    """Display score breakdown for a stock."""
    console.print(f"\n[bold blue]Analyzing {symbol}...[/bold blue]\n")

    fundamentals = agent.data_fetcher.get_fundamental_data(symbol)
    if not fundamentals:
        console.print(f"[red]Could not fetch data for {symbol}[/red]")
        return

    fund_analysis = agent.fundamental_analyzer.analyze_stock(fundamentals)

    console.print(f"[bold cyan]{fundamentals.get('name', symbol)}[/bold cyan]")
    console.print(f"[dim]{symbol}[/dim]\n")

    table = Table(title="Score Breakdown", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Score", justify="right", style="yellow")
    table.add_column("Rating", style="green")

    def get_rating(score):
        if score >= 80:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        else:
            return "Poor"

    overall = fund_analysis.get('overall_score', 0)
    table.add_row("[bold]Overall Score[/bold]", f"[bold]{overall:.1f}/100[/bold]", f"[bold]{get_rating(overall)}[/bold]")
    table.add_row("", "", "")

    table.add_row("Growth", f"{fund_analysis.get('growth_score', 0):.1f}/100", get_rating(fund_analysis.get('growth_score', 0)))
    table.add_row("Valuation", f"{fund_analysis.get('valuation_score', 0):.1f}/100", get_rating(fund_analysis.get('valuation_score', 0)))
    table.add_row("Profitability", f"{fund_analysis.get('profitability_score', 0):.1f}/100", get_rating(fund_analysis.get('profitability_score', 0)))
    table.add_row("Financial Health", f"{fund_analysis.get('financial_health_score', 0):.1f}/100", get_rating(fund_analysis.get('financial_health_score', 0)))
    table.add_row("Quality", f"{fund_analysis.get('quality_score', 0):.1f}/100", get_rating(fund_analysis.get('quality_score', 0)))

    console.print(table)

    signal = fund_analysis.get('buy_signal', 'hold')
    signal_color = 'green' if signal in ['buy', 'strong_buy'] else 'yellow'
    console.print(f"\n[bold {signal_color}]Signal: {signal.upper()}[/bold {signal_color}]")
    console.print(f"Risk Level: {fund_analysis.get('risk_level', 'unknown')}")
    console.print()


def display_favorites(favorites):
    """Display favorites in a table."""
    table = Table(title="Favorite Stocks", show_header=True, header_style="bold magenta")
    table.add_column("Symbol", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Category", style="yellow")
    table.add_column("Added", style="dim")

    for fav in favorites:
        table.add_row(
            fav['symbol'],
            fav['name'] or '',
            fav['category'],
            fav['added_date'][:10]
        )

    console.print(table)
    console.print(f"\nTotal: {len(favorites)} favorites\n")


def display_categories(categories):
    """Display categories."""
    table = Table(title="Favorite Categories", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Stocks", justify="right", style="yellow")

    for cat in categories:
        table.add_row(
            cat['name'],
            cat['description'] or '',
            str(cat['count'])
        )

    console.print(table)
    console.print()


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
