"""Help system for the Investment Agent CLI."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns

console = Console()


class HelpSystem:
    """Display help information for CLI commands."""

    @staticmethod
    def show_all():
        """Display all available commands."""
        console.print("\n")
        console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
        console.print("[bold cyan]        INVESTMENT AGENT - COMMAND REFERENCE               [/bold cyan]")
        console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
        console.print("\n")

        # Show command categories
        HelpSystem._show_analysis_commands()
        HelpSystem._show_market_commands()
        HelpSystem._show_screening_commands()
        HelpSystem._show_portfolio_commands()
        HelpSystem._show_favorites_commands()
        HelpSystem._show_data_commands()
        HelpSystem._show_utility_commands()

        console.print("\n[bold yellow]💡 Tips:[/bold yellow]")
        console.print("  • Use [cyan]help <command>[/cyan] for detailed help on a specific command")
        console.print("  • Most commands support [cyan]--help[/cyan] flag")
        console.print("  • Commands are case-insensitive")
        console.print("\n")

    @staticmethod
    def _show_analysis_commands():
        """Show stock analysis commands."""
        table = Table(title="📊 STOCK ANALYSIS COMMANDS", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=30)
        table.add_column("Description", style="white")

        table.add_row("analyze <ticker>", "Deep dive analysis of a single stock")
        table.add_row("info <ticker>", "Quick snapshot (price, market cap, score)")
        table.add_row("score <ticker>", "Show growth score breakdown")
        table.add_row("buy <ticker>", "Evaluate buying a stock")
        table.add_row("sell <ticker>", "Evaluate selling a stock")

        console.print(table)
        console.print()

    @staticmethod
    def _show_market_commands():
        """Show market scanning commands."""
        table = Table(title="🌍 MARKET COMMANDS", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=30)
        table.add_column("Description", style="white")

        table.add_row("scan", "Scan markets for opportunities")
        table.add_row("scan --markets TSX NASDAQ", "Scan specific markets")
        table.add_row("ai", "Scan ALL AI companies")
        table.add_row("ai --market USA", "Scan AI companies in USA")
        table.add_row("ai --market CANADA", "Scan AI companies in Canada")
        table.add_row("ai --market INDIA", "Scan AI companies in India")
        table.add_row("sector <name>", "Scan specific sector (e.g., Fintech)")
        table.add_row("india", "Scan Indian market (NSE)")
        table.add_row("canada", "Scan Canadian market (TSX)")
        table.add_row("us", "Scan US market (NASDAQ/NYSE)")

        console.print(table)
        console.print()

    @staticmethod
    def _show_screening_commands():
        """Show screening commands."""
        table = Table(title="🔍 SCREENING & FILTERING", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=30)
        table.add_column("Description", style="white")

        table.add_row("recommend", "Get investment recommendations")
        table.add_row("recommend --focus growth", "Growth stock recommendations")
        table.add_row("recommend --focus value", "Value stock recommendations")
        table.add_row("recommend --focus breakout", "Breakout stock recommendations")
        table.add_row("top <N>", "Show top N opportunities")
        table.add_row("top <N> --market USA", "Top N stocks in specific market")

        console.print(table)
        console.print()

    @staticmethod
    def _show_portfolio_commands():
        """Show portfolio management commands."""
        table = Table(title="💼 PORTFOLIO MANAGEMENT", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=30)
        table.add_column("Description", style="white")

        table.add_row("portfolio", "Show complete portfolio overview")
        table.add_row("daily", "Run daily routine (scan + monitor)")
        table.add_row("positions", "List all current positions")
        table.add_row("performance", "Portfolio performance metrics")

        console.print(table)
        console.print()

    @staticmethod
    def _show_favorites_commands():
        """Show favorites management commands."""
        table = Table(title="⭐ FAVORITES MANAGEMENT", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=30)
        table.add_column("Description", style="white")

        table.add_row("fav add <ticker>", "Add stock to favorites")
        table.add_row("fav add <ticker> <category>", "Add to specific category")
        table.add_row("fav remove <ticker>", "Remove from favorites")
        table.add_row("fav show", "Show all favorites")
        table.add_row("fav show <category>", "Show favorites in category")
        table.add_row("fav scan", "Scan all favorites for signals")
        table.add_row("fav export", "Export favorites to file")

        console.print(table)
        console.print()

    @staticmethod
    def _show_utility_commands():
        """Show utility commands."""
        table = Table(title="🔧 UTILITY COMMANDS", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=30)
        table.add_column("Description", style="white")

        table.add_row("help", "Show this help message")
        table.add_row("help <command>", "Help on specific command")
        table.add_row("version", "Show version information")
        table.add_row("status", "Show system status")
        table.add_row("quick", "Quick start guide")

        console.print(table)
        console.print()

    @staticmethod
    def _show_data_commands():
        """Show data management commands."""
        table = Table(title="💾 DATA MANAGEMENT", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=30)
        table.add_column("Description", style="white")

        table.add_row("list", "List all stocks numbered by country")
        table.add_row("list --market USA", "List stocks from specific market")
        table.add_row("list --cached", "Show only cached stocks")
        table.add_row("refresh", "Refresh all stock data")
        table.add_row("refresh --stale", "Refresh only stale data (>24h)")
        table.add_row("refresh --numbers 1,5,10-15", "Refresh specific numbered stocks")
        table.add_row("refresh --market USA", "Refresh all stocks in market")
        table.add_row("cache stats", "Show cache statistics")
        table.add_row("cache clear", "Clear all cached data")

        console.print(table)
        console.print()

    @staticmethod
    def show_command_help(command: str):
        """Show detailed help for a specific command."""
        help_text = {
            'analyze': """
[bold cyan]analyze <ticker>[/bold cyan]

Perform comprehensive analysis of a stock including:
  • Fundamental analysis (growth, valuation, profitability)
  • Technical analysis (trends, indicators, signals)
  • Risk assessment
  • Growth potential estimation

[bold yellow]Examples:[/bold yellow]
  python main.py analyze NVDA
  python main.py analyze TCS.NS
  python main.py analyze SHOP.TO
""",
            'ai': """
[bold cyan]ai [--market MARKET] [--min-score SCORE][/bold cyan]

Scan AI companies across markets.

[bold yellow]Options:[/bold yellow]
  --market USA|CANADA|INDIA|ALL  Market to scan (default: ALL)
  --min-score SCORE              Minimum score threshold (default: 65)

[bold yellow]Examples:[/bold yellow]
  python main.py ai
  python main.py ai --market USA --min-score 70
  python main.py ai --market INDIA
""",
            'sector': """
[bold cyan]sector <sector_name> [--market MARKET] [--min-score SCORE][/bold cyan]

Scan specific sector for opportunities.

[bold yellow]Available Sectors:[/bold yellow]
  • Fintech
  • Cloud Computing
  • Cybersecurity
  • IT Services
  • EV & Clean Energy
  • Healthcare
  • E-commerce

[bold yellow]Examples:[/bold yellow]
  python main.py sector Fintech
  python main.py sector "Cloud Computing" --market USA
  python main.py sector "IT Services" --market INDIA
""",
            'scan': """
[bold cyan]scan [--markets MARKET [MARKET ...]][/bold cyan]

Scan markets for high-growth opportunities.

[bold yellow]Options:[/bold yellow]
  --markets    Markets to scan (TSX, NASDAQ, NYSE, NSE, BSE)

[bold yellow]Examples:[/bold yellow]
  python main.py scan
  python main.py scan --markets TSX NASDAQ
  python main.py scan --markets NSE BSE
""",
            'recommend': """
[bold cyan]recommend [--focus FOCUS] [--min-score SCORE][/bold cyan]

Get investment recommendations based on strategy.

[bold yellow]Options:[/bold yellow]
  --focus growth|value|breakout  Recommendation focus (default: growth)
  --min-score SCORE             Minimum score (default: 70)

[bold yellow]Examples:[/bold yellow]
  python main.py recommend
  python main.py recommend --focus breakout
  python main.py recommend --min-score 75
""",
            'buy': """
[bold cyan]buy <ticker> [--shares N][/bold cyan]

Evaluate buying a stock with entry analysis.

[bold yellow]Provides:[/bold yellow]
  • Buy recommendation (BUY/HOLD/SKIP)
  • Position size calculation
  • Entry price and stop-loss levels
  • Expected returns
  • Risk assessment

[bold yellow]Examples:[/bold yellow]
  python main.py buy NVDA
  python main.py buy TCS.NS --shares 100
""",
            'sell': """
[bold cyan]sell <ticker>[/bold cyan]

Evaluate selling a position with exit analysis.

[bold yellow]Provides:[/bold yellow]
  • Sell recommendation (SELL/HOLD)
  • Current position details
  • Profit/loss calculation
  • Exit reasons (if any)
  • Technical/fundamental signals

[bold yellow]Examples:[/bold yellow]
  python main.py sell SHOP.TO
  python main.py sell INFY.NS
""",
            'portfolio': """
[bold cyan]portfolio[/bold cyan]

Show complete portfolio overview including:
  • All positions with current values
  • Cash balance
  • Total portfolio value
  • Overall returns
  • Position sizes and allocations

[bold yellow]Example:[/bold yellow]
  python main.py portfolio
""",
            'daily': """
[bold cyan]daily[/bold cyan]

Run daily routine:
  1. Scan markets for new opportunities
  2. Monitor existing positions for exit signals
  3. Generate portfolio summary
  4. Identify position alerts

[bold yellow]Example:[/bold yellow]
  python main.py daily
""",
            'list': """
[bold cyan]list [--market MARKET] [--cached][/bold cyan]

List all stocks numbered by country with cache status.

[bold yellow]Options:[/bold yellow]
  --market USA|CANADA|INDIA|ALL  Filter by market (default: ALL)
  --cached                       Show only cached stocks

[bold yellow]Output:[/bold yellow]
  • Sequential numbering across all markets
  • Stock symbol, name, and category
  • Cache status (Fresh, Aged, Stale, Not cached)

[bold yellow]Examples:[/bold yellow]
  python main.py list
  python main.py list --market USA
  python main.py list --cached

[bold yellow]Use Case:[/bold yellow]
  Use the numbers shown to refresh specific stocks:
  python main.py refresh --numbers 1,5,10-15
""",
            'refresh': """
[bold cyan]refresh [symbols] [--numbers NUMS] [--market MARKET] [--stale] [--force][/bold cyan]

Refresh stock data to keep cache up-to-date.

[bold yellow]Options:[/bold yellow]
  symbols                        Specific symbols to refresh (e.g., NVDA TCS.NS)
  --numbers 1,5,10-15           Refresh by numbers from list command
  --market USA|CANADA|INDIA     Refresh all stocks in market
  --stale                       Refresh only stale data (>24h old)
  --force                       Force refresh even if recently cached

[bold yellow]Examples:[/bold yellow]
  python main.py refresh                    # Refresh all stocks
  python main.py refresh --stale            # Refresh only stale data
  python main.py refresh --market USA       # Refresh all US stocks
  python main.py refresh --numbers 1,5,10-15  # Refresh specific numbered stocks
  python main.py refresh NVDA PLTR          # Refresh specific symbols
  python main.py refresh --numbers 1-10 --force  # Force refresh first 10

[bold yellow]Performance:[/bold yellow]
  • Fresh data (<1h): Skipped unless --force
  • Aged data (1-24h): Refreshed by default
  • Stale data (>24h): Always refreshed
  • Rate limiting: 0.5s delay between stocks
""",
            'cache': """
[bold cyan]cache stats[/bold cyan]
[bold cyan]cache clear [symbol][/bold cyan]

Manage data cache and view statistics.

[bold yellow]Commands:[/bold yellow]
  stats     Show cache statistics and refresh history
  clear     Clear cached data (all or specific symbol)

[bold yellow]Statistics Include:[/bold yellow]
  • Total cached stocks
  • Fresh (<1h), Aged (1-24h), Stale (>24h) counts
  • Breakdown by market
  • Recent refresh history

[bold yellow]Examples:[/bold yellow]
  python main.py cache stats        # Show cache statistics
  python main.py cache clear        # Clear all cache (prompts for confirmation)
  python main.py cache clear NVDA   # Clear cache for specific stock

[bold yellow]Use Cases:[/bold yellow]
  • Monitor cache health before/after refresh
  • Clear stale data to force fresh fetches
  • Track refresh history and performance
""",
        }

        if command.lower() in help_text:
            console.print(Panel(help_text[command.lower()], border_style="cyan"))
        else:
            console.print(f"[yellow]No detailed help available for '{command}'[/yellow]")
            console.print("Use [cyan]help[/cyan] to see all available commands")

    @staticmethod
    def show_quick_start():
        """Show quick start guide."""
        console.print("\n")
        console.print(Panel.fit(
            "[bold cyan]INVESTMENT AGENT - QUICK START GUIDE[/bold cyan]",
            border_style="cyan"
        ))

        console.print("\n[bold yellow]🚀 Getting Started in 3 Steps:[/bold yellow]\n")

        console.print("[bold]1. Scan for Opportunities[/bold]")
        console.print("   [cyan]python main.py ai[/cyan]                    # Scan all AI companies")
        console.print("   [cyan]python main.py scan[/cyan]                  # General market scan")
        console.print("   [cyan]python main.py india[/cyan]                 # Scan Indian market")
        console.print()

        console.print("[bold]2. Analyze Stocks[/bold]")
        console.print("   [cyan]python main.py analyze NVDA[/cyan]          # Analyze NVIDIA")
        console.print("   [cyan]python main.py analyze TCS.NS[/cyan]        # Analyze TCS (India)")
        console.print("   [cyan]python main.py info SHOP.TO[/cyan]          # Quick info on Shopify")
        console.print()

        console.print("[bold]3. Get Recommendations[/bold]")
        console.print("   [cyan]python main.py recommend[/cyan]             # Get recommendations")
        console.print("   [cyan]python main.py buy PLTR[/cyan]              # Evaluate buying")
        console.print()

        console.print("[bold yellow]📚 Learn More:[/bold yellow]")
        console.print("   [cyan]python main.py help[/cyan]                  # All commands")
        console.print("   [cyan]python main.py help analyze[/cyan]          # Help on specific command")
        console.print()

        console.print("[bold yellow]💡 Pro Tips:[/bold yellow]")
        console.print("   • Use [cyan]--market[/cyan] flag to focus on specific markets")
        console.print("   • Add [cyan]--min-score[/cyan] to filter by quality")
        console.print("   • Run [cyan]daily[/cyan] command each morning for routine scan")
        console.print()

    @staticmethod
    def show_version():
        """Show version information."""
        from .. import __version__

        console.print("\n")
        console.print(Panel.fit(
            f"[bold cyan]Investment Agent v{__version__}[/bold cyan]\n"
            "[white]AI-Powered Investment Analysis & Portfolio Management[/white]\n\n"
            "[yellow]Markets:[/yellow] USA 🇺🇸 | Canada 🇨🇦 | India 🇮🇳\n"
            "[yellow]Companies:[/yellow] 200+ tracked | 50+ AI companies\n"
            "[yellow]Sectors:[/yellow] 10+ high-growth sectors\n\n"
            "[dim]For help: python main.py help[/dim]",
            border_style="cyan"
        ))
        console.print()


__all__ = ['HelpSystem']
