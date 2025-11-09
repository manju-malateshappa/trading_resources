"""
Basic usage examples for the Investment Agent.

This script demonstrates common use cases.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from investment_agent.agent import InvestmentAgent
from investment_agent.utils.logger import logger


def example_1_scan_market():
    """Example 1: Scan market for high-growth opportunities."""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 1: Scan Market for Opportunities")
    logger.info("=" * 60)

    # Initialize agent
    agent = InvestmentAgent(portfolio_name="Example Portfolio")

    # Scan Canadian market (TSX)
    opportunities = agent.scan_market(markets=['TSX'])

    # Display top 5 opportunities
    if not opportunities.empty:
        top_5 = opportunities.head(5)
        logger.info("\nTop 5 Opportunities:")
        for _, stock in top_5.iterrows():
            logger.info(f"\n{stock['symbol']} - {stock['name']}")
            logger.info(f"  Score: {stock['overall_score']:.1f}/100")
            logger.info(f"  Recommendation: {stock['recommendation']}")
            logger.info(f"  Expected 2Y Return: {stock['expected_return_2y']:.1%}")
            logger.info(f"  Risk Level: {stock['risk_level']}")


def example_2_analyze_stock():
    """Example 2: Perform detailed analysis of a specific stock."""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 2: Analyze Specific Stock")
    logger.info("=" * 60)

    agent = InvestmentAgent()

    # Analyze Shopify (Canadian tech stock)
    symbol = "SHOP.TO"
    analysis = agent.analyze_stock(symbol)

    # Analysis results are automatically displayed by the agent


def example_3_evaluate_buy():
    """Example 3: Evaluate buying a stock."""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 3: Evaluate Buy Decision")
    logger.info("=" * 60)

    agent = InvestmentAgent()

    # Evaluate buying Lightspeed Commerce
    symbol = "LSPD.TO"
    evaluation = agent.evaluate_buy(symbol)

    if evaluation['action'] == 'BUY':
        logger.info(f"\nRecommendation: BUY {evaluation['shares']} shares")
        logger.info(f"Entry Price: ${evaluation['current_price']:.2f}")
        logger.info(f"Total Investment: ${evaluation['total_cost']:,.2f}")
        logger.info(f"Stop Loss: ${evaluation['stop_loss']:.2f}")


def example_4_get_recommendations():
    """Example 4: Get different types of recommendations."""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 4: Get Investment Recommendations")
    logger.info("=" * 60)

    agent = InvestmentAgent()

    # Growth recommendations (high revenue growth potential)
    logger.info("\n--- GROWTH STOCKS ---")
    growth_stocks = agent.get_recommendations(min_score=70.0, focus='growth')

    # Value opportunities (undervalued with high growth)
    logger.info("\n--- VALUE OPPORTUNITIES ---")
    value_stocks = agent.get_recommendations(focus='value')

    # Breakout candidates (strong technical momentum)
    logger.info("\n--- BREAKOUT CANDIDATES ---")
    breakout_stocks = agent.get_recommendations(focus='breakout')


def example_5_daily_routine():
    """Example 5: Run daily investment routine."""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 5: Daily Routine")
    logger.info("=" * 60)

    agent = InvestmentAgent()

    # Run daily routine: scan market + monitor positions
    results = agent.daily_routine()

    logger.info(f"\nDaily routine completed!")
    logger.info(f"Opportunities found: {len(results['opportunities']) if results['opportunities'] is not None else 0}")
    logger.info(f"Position alerts: {len(results['position_alerts'])}")
    logger.info(f"Portfolio value: ${results['portfolio_summary']['total_value']:,.2f}")
    logger.info(f"Portfolio return: {results['portfolio_summary']['return']:.2%}")


def example_6_portfolio_simulation():
    """Example 6: Simulate building a portfolio."""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 6: Portfolio Simulation")
    logger.info("=" * 60)

    agent = InvestmentAgent(portfolio_name="Simulation Portfolio")

    # Get top recommendations
    recommendations = agent.get_recommendations(min_score=75.0, focus='growth')

    if recommendations.empty:
        logger.info("No recommendations found")
        return

    # Simulate buying top 5 stocks
    logger.info("\nSimulating purchases of top 5 stocks...")

    for idx, (_, stock) in enumerate(recommendations.head(5).iterrows(), 1):
        symbol = stock['symbol']
        logger.info(f"\n{idx}. Evaluating {symbol}...")

        evaluation = agent.evaluate_buy(symbol)

        if evaluation['action'] == 'BUY':
            logger.info(f"   Would buy {evaluation['shares']} shares at ${evaluation['current_price']:.2f}")
            logger.info(f"   Investment: ${evaluation['total_cost']:,.2f}")
            logger.info(f"   Expected 2Y return: {evaluation['expected_return_2y']:.1%}")

            # In a real scenario, you would execute:
            # agent.portfolio.add_position(
            #     symbol,
            #     evaluation['shares'],
            #     evaluation['current_price']
            # )
        else:
            logger.info(f"   SKIP: {evaluation.get('reason', 'Does not meet criteria')}")


def main():
    """Run all examples."""
    logger.info("\n" + "=" * 80)
    logger.info("INVESTMENT AGENT - USAGE EXAMPLES")
    logger.info("=" * 80)

    # Choose which examples to run
    examples = [
        ("Scan Market", example_1_scan_market),
        ("Analyze Stock", example_2_analyze_stock),
        ("Evaluate Buy", example_3_evaluate_buy),
        ("Get Recommendations", example_4_get_recommendations),
        ("Daily Routine", example_5_daily_routine),
        ("Portfolio Simulation", example_6_portfolio_simulation),
    ]

    logger.info("\nAvailable Examples:")
    for idx, (name, _) in enumerate(examples, 1):
        logger.info(f"{idx}. {name}")

    logger.info("\n" + "=" * 80)
    logger.info("Running Example 1: Scan Market")
    logger.info("=" * 80)

    # Run first example by default
    # To run a different example, change the index below
    examples[0][1]()  # Runs example_1_scan_market

    logger.info("\n" + "=" * 80)
    logger.info("To run other examples, modify the examples index in main()")
    logger.info("=" * 80)


if __name__ == '__main__':
    main()
