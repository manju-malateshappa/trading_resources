#!/usr/bin/env python3
"""
Investment Agent - Main CLI Interface

A comprehensive AI-powered investment analysis and portfolio management system
focused on identifying high-growth small/mid-cap stocks for 100-200% returns.
"""

import argparse
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List

# Add the project directory to path
sys.path.insert(0, str(Path(__file__).parent))

from investment_agent.agent import InvestmentAgent
from investment_agent.utils.logger import logger
from investment_agent.utils import HelpSystem, favorites_manager, data_cache
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

    # List stocks command
    list_parser = subparsers.add_parser('list', help='List all stocks by country')
    list_parser.add_argument('--market', choices=['USA', 'CANADA', 'INDIA', 'ALL'], default='ALL', help='Filter by market')
    list_parser.add_argument('--cached', action='store_true', help='Show only cached stocks')

    # Refresh data commands
    refresh_parser = subparsers.add_parser('refresh', help='Refresh stock data')
    refresh_parser.add_argument('symbols', nargs='*', help='Specific symbols to refresh (or leave empty for all)')
    refresh_parser.add_argument('--numbers', help='Refresh by numbers from list (e.g., 1,5,10-15)')
    refresh_parser.add_argument('--market', choices=['USA', 'CANADA', 'INDIA'], help='Refresh all in market')
    refresh_parser.add_argument('--stale', action='store_true', help='Refresh only stale data (>24h)')
    refresh_parser.add_argument('--force', action='store_true', help='Force refresh even if recent')

    # Cache management
    cache_parser = subparsers.add_parser('cache', help='Manage data cache')
    cache_subparsers = cache_parser.add_subparsers(dest='cache_command', help='Cache commands')

    cache_stats_parser = cache_subparsers.add_parser('stats', help='Show cache statistics')
    cache_clear_parser = cache_subparsers.add_parser('clear', help='Clear cache')
    cache_clear_parser.add_argument('symbol', nargs='?', help='Specific symbol to clear')

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

    elif args.command == 'list':
        handle_list_command(args)

    elif args.command == 'refresh':
        handle_refresh_command(agent, args)

    elif args.command == 'cache':
        handle_cache_command(args)


def handle_list_command(args):
    """Handle list stocks command."""
    console.print("\n[bold cyan]📊 Stock Database - Company List[/bold cyan]\n")

    # Get symbols from company database
    if args.market == 'ALL':
        usa_symbols = company_db.get_all_symbols(market='USA')
        canada_symbols = company_db.get_all_symbols(market='CANADA')
        india_symbols = company_db.get_all_symbols(market='INDIA')

        all_stocks = []
        for symbol in usa_symbols:
            info = company_db.get_company_info(symbol)
            all_stocks.append({**info, 'symbol': symbol, 'market': 'USA'})

        for symbol in canada_symbols:
            info = company_db.get_company_info(symbol)
            all_stocks.append({**info, 'symbol': symbol, 'market': 'CANADA'})

        for symbol in india_symbols:
            info = company_db.get_company_info(symbol)
            all_stocks.append({**info, 'symbol': symbol, 'market': 'INDIA'})

    else:
        symbols = company_db.get_all_symbols(market=args.market)
        all_stocks = []
        for symbol in symbols:
            info = company_db.get_company_info(symbol)
            all_stocks.append({**info, 'symbol': symbol, 'market': args.market})

    # Filter by cached if requested
    if args.cached:
        cached_symbols = {item['symbol'] for item in data_cache.get_all_cached_symbols()}
        all_stocks = [s for s in all_stocks if s['symbol'] in cached_symbols]

    # Group by market
    markets = {}
    for stock in all_stocks:
        market = stock.get('market', 'Unknown')
        if market not in markets:
            markets[market] = []
        markets[market].append(stock)

    # Display by market
    total_count = 0
    number = 1

    for market in sorted(markets.keys()):
        stocks = markets[market]

        table = Table(title=f"{market} Stocks", show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=5)
        table.add_column("Symbol", style="cyan", width=12)
        table.add_column("Name", style="white", width=35)
        table.add_column("Category", style="yellow", width=18)
        table.add_column("Status", style="green", width=12)

        for stock in sorted(stocks, key=lambda x: x['symbol']):
            # Check if cached
            cached_data = data_cache.get_cached_data(stock['symbol'])
            if cached_data:
                cache_age = (datetime.now() - datetime.fromisoformat(cached_data['cache_updated'])).total_seconds() / 3600
                if cache_age < 1:
                    status = "[green]Fresh[/green]"
                elif cache_age < 24:
                    status = f"[yellow]{cache_age:.0f}h old[/yellow]"
                else:
                    status = "[red]Stale[/red]"
            else:
                status = "[dim]Not cached[/dim]"

            table.add_row(
                str(number),
                stock['symbol'],
                stock.get('name', '')[:35],
                stock.get('category', '')[:18],
                status
            )
            number += 1

        console.print(table)
        console.print()
        total_count += len(stocks)

    console.print(f"[bold]Total: {total_count} stocks[/bold]")
    console.print("\n[dim]💡 Tip: Use [cyan]refresh --numbers 1,5,10-15[/cyan] to refresh specific stocks[/dim]\n")


def handle_refresh_command(agent, args):
    """Handle refresh data command."""
    from datetime import datetime

    console.print("\n[bold cyan]🔄 Refreshing Stock Data[/bold cyan]\n")

    symbols_to_refresh = []

    # Determine which symbols to refresh
    if args.numbers:
        # Refresh by numbers from list
        symbols_to_refresh = get_symbols_by_numbers(args.numbers)

    elif args.market:
        # Refresh all in market
        symbols_to_refresh = company_db.get_all_symbols(market=args.market)
        console.print(f"[yellow]Refreshing all {len(symbols_to_refresh)} stocks in {args.market}...[/yellow]\n")

    elif args.stale:
        # Refresh only stale data
        symbols_to_refresh = data_cache.get_stale_symbols(max_age_hours=24)
        console.print(f"[yellow]Refreshing {len(symbols_to_refresh)} stale stocks...[/yellow]\n")

    elif args.symbols:
        # Specific symbols provided
        symbols_to_refresh = [s.upper() for s in args.symbols]

    else:
        # Refresh all
        symbols_to_refresh = company_db.get_all_symbols()
        console.print(f"[yellow]⚠️  Refreshing ALL {len(symbols_to_refresh)} stocks - this may take a while![/yellow]\n")

    if not symbols_to_refresh:
        console.print("[yellow]No symbols to refresh[/yellow]")
        return

    # Perform refresh
    start_time = time.time()
    successful = 0
    failed = 0

    with console.status("[bold green]Refreshing data...") as status:
        for i, symbol in enumerate(symbols_to_refresh, 1):
            # Skip if recently cached and not forcing
            if not args.force and not data_cache.is_stale(symbol, max_age_hours=1):
                status.update(f"[dim]Skipping {symbol} (recently cached)[/dim]")
                successful += 1
                continue

            status.update(f"[green]Refreshing {i}/{len(symbols_to_refresh)}: {symbol}[/green]")

            try:
                # Fetch fresh data
                fundamentals = agent.data_fetcher.get_fundamental_data(symbol)

                if fundamentals and fundamentals.get('current_price'):
                    # Cache the data
                    data_cache.cache_data(
                        symbol,
                        fundamentals,
                        name=fundamentals.get('name'),
                        market=fundamentals.get('market', 'Unknown')
                    )
                    successful += 1
                else:
                    logger.warning(f"No data returned for {symbol}")
                    failed += 1

                # Rate limiting
                time.sleep(0.5)

            except Exception as e:
                logger.error(f"Error refreshing {symbol}: {str(e)}")
                failed += 1

    duration = time.time() - start_time

    # Record refresh
    data_cache.record_refresh(len(symbols_to_refresh), successful, failed, duration)

    # Display results
    console.print(f"\n[bold green]✓ Refresh Complete![/bold green]")
    console.print(f"  Total: {len(symbols_to_refresh)}")
    console.print(f"  [green]Successful: {successful}[/green]")
    console.print(f"  [red]Failed: {failed}[/red]")
    console.print(f"  Duration: {duration:.1f}s")
    console.print()


def get_symbols_by_numbers(numbers_str: str) -> List[str]:
    """Parse number ranges and return symbols.

    Args:
        numbers_str: e.g., "1,5,10-15"

    Returns:
        List of symbols
    """
    # Get all symbols with their numbers
    all_stocks = []
    number = 1

    for market in ['USA', 'CANADA', 'INDIA']:
        symbols = company_db.get_all_symbols(market=market)
        for symbol in sorted(symbols):
            all_stocks.append((number, symbol))
            number += 1

    # Parse numbers
    selected_numbers = set()

    for part in numbers_str.split(','):
        part = part.strip()
        if '-' in part:
            # Range like "10-15"
            start, end = part.split('-')
            selected_numbers.update(range(int(start), int(end) + 1))
        else:
            # Single number
            selected_numbers.add(int(part))

    # Get symbols
    selected_symbols = []
    for num, symbol in all_stocks:
        if num in selected_numbers:
            selected_symbols.append(symbol)

    console.print(f"[green]Selected {len(selected_symbols)} stocks: {', '.join(selected_symbols[:10])}{('...' if len(selected_symbols) > 10 else '')}[/green]\n")

    return selected_symbols


def handle_cache_command(args):
    """Handle cache management commands."""
    if not args.cache_command:
        # Show cache stats
        args.cache_command = 'stats'

    if args.cache_command == 'stats':
        stats = data_cache.get_cache_stats()

        console.print("\n[bold cyan]📦 Cache Statistics[/bold cyan]\n")

        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="yellow")
        table.add_column("Value", style="white")

        table.add_row("Total Cached", str(stats['total']))
        table.add_row("Fresh (<1h)", f"[green]{stats['fresh']}[/green]")
        table.add_row("Aged (1-24h)", f"[yellow]{stats['aged']}[/yellow]")
        table.add_row("Stale (>24h)", f"[red]{stats['stale']}[/red]")

        console.print(table)

        if stats['by_market']:
            console.print("\n[bold]By Market:[/bold]")
            for market, count in stats['by_market'].items():
                console.print(f"  {market}: {count}")

        # Show recent refresh history
        history = data_cache.get_refresh_history(limit=5)
        if history:
            console.print("\n[bold]Recent Refreshes:[/bold]")
            for record in history:
                console.print(f"  {record['date'][:19]}: {record['successful']}/{record['total']} successful ({record['duration']:.1f}s)")

        console.print()

    elif args.cache_command == 'clear':
        if args.symbol:
            count = data_cache.clear_cache(symbol=args.symbol)
            console.print(f"[green]✓[/green] Cleared cache for {args.symbol}")
        else:
            console.print("[yellow]⚠️  This will clear ALL cached data. Are you sure? (y/N)[/yellow]")
            response = input().strip().lower()
            if response == 'y':
                count = data_cache.clear_cache()
                console.print(f"[green]✓[/green] Cleared {count} cached records")
            else:
                console.print("[yellow]Cancelled[/yellow]")


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
