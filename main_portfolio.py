"""Enhanced main entry point with portfolio analysis support."""
import sys
import logging
from stock_research_crew.crew import stock_crew
from stock_research_crew.portfolio_analyzer import PortfolioAnalyzer
from stock_research_crew.cache import cache_manager
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Config.CACHE_DIR / 'app.log')
    ]
)
logger = logging.getLogger(__name__)


def validate_stock_input(stock_name: str) -> bool:
    """Validate stock input."""
    if not stock_name or not stock_name.strip():
        return False
    if len(stock_name) > 100:
        return False
    return True


def print_report(result: str, title: str = "STOCK RESEARCH REPORT"):
    """Print formatted report."""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80)
    print(result)
    print("=" * 80)


def analyze_single_stock():
    """Analyze a single stock."""
    stock_name = input("\nEnter stock name or ticker: ").strip()
    
    if not validate_stock_input(stock_name):
        logger.error("Invalid stock input")
        print("Error: Please enter a valid stock name or ticker")
        return 1
    
    logger.info(f"Processing stock: {stock_name}")
    
    # Check cache
    cached = cache_manager.get_cached_result(stock_name)
    if cached:
        print(f"\n✓ Using cached result (saved within last {Config.CACHE_EXPIRY_HOURS} hours)")
        print_report(cached)
        return 0
    
    # Run crew
    print(f"\n⚙ Running analysis for {stock_name}...")
    print(f"  Model: {Config.LLM_MODEL}")
    print(f"  This may take several minutes...\n")
    
    try:
        result = stock_crew.kickoff(inputs={"stock": stock_name})
        output = str(result)
        
        # Save to cache
        cache_manager.save_result(stock_name, output)
        logger.info(f"Analysis completed and cached for {stock_name}")
        
        # Print result
        print_report(output)
        
        print(f"\n✓ Analysis complete. Results cached for {Config.CACHE_EXPIRY_HOURS} hours.")
        return 0
        
    except Exception as e:
        logger.error(f"Crew execution failed: {e}", exc_info=True)
        print(f"\n✗ Error during analysis: {e}")
        print("  Check that Ollama is running and the model is available.")
        return 1


def analyze_portfolio():
    """Analyze multiple stocks as a portfolio."""
    print("\n📊 Portfolio Analysis Mode")
    print("=" * 80)
    
    # Get stocks
    stocks_input = input("\nEnter stock tickers separated by commas (e.g., AAPL, GOOGL, MSFT): ").strip()
    stocks = [s.strip().upper() for s in stocks_input.split(",") if s.strip()]
    
    if len(stocks) < 2:
        print("Error: Please enter at least 2 stocks for portfolio analysis")
        return 1
    
    # Validate stocks
    for stock in stocks:
        if not validate_stock_input(stock):
            print(f"Error: Invalid stock ticker '{stock}'")
            return 1
    
    # Get portfolio size
    portfolio_input = input(f"\nEnter portfolio size in USD (default: $100,000): ").strip()
    try:
        portfolio_size = float(portfolio_input) if portfolio_input else 100000
        if portfolio_size <= 0:
            print("Error: Portfolio size must be positive")
            return 1
    except ValueError:
        print("Error: Invalid portfolio size")
        return 1
    
    # Ask about parallel processing
    parallel_input = input("\nUse parallel processing? (y/n, default: n): ").strip().lower()
    parallel = parallel_input == 'y'
    
    print(f"\n⚙ Analyzing portfolio of {len(stocks)} stocks...")
    print(f"  Stocks: {', '.join(stocks)}")
    print(f"  Portfolio Size: ${portfolio_size:,.0f}")
    print(f"  Parallel Processing: {'Yes' if parallel else 'No'}")
    print(f"  Model: {Config.LLM_MODEL}")
    print(f"  This may take several minutes...\n")
    
    try:
        # Create analyzer
        analyzer = PortfolioAnalyzer(stocks, portfolio_size)
        
        # Generate full report
        report = analyzer.generate_full_report(parallel=parallel)
        
        # Print individual analyses
        print("\n" + "=" * 80)
        print("INDIVIDUAL STOCK ANALYSES".center(80))
        print("=" * 80)
        
        for stock, result in report["individual_analyses"].items():
            print(f"\n{'─' * 80}")
            print(f"  {stock}")
            print(f"{'─' * 80}")
            print(result)
        
        # Print portfolio analysis
        print_report(report["portfolio_analysis"], "PORTFOLIO ANALYSIS & ALLOCATION")
        
        print(f"\n✓ Portfolio analysis complete!")
        print(f"  Stocks analyzed: {len(stocks)}")
        print(f"  Portfolio size: ${portfolio_size:,.0f}")
        print(f"  Performance logs: {Config.PROFILE_FILE}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Portfolio analysis failed: {e}", exc_info=True)
        print(f"\n✗ Error during portfolio analysis: {e}")
        return 1


def main():
    """Main execution function."""
    try:
        print("\n" + "=" * 80)
        print("AI STOCK RESEARCH CREW".center(80))
        print("=" * 80)
        print("\nSelect analysis mode:")
        print("  1. Single Stock Analysis")
        print("  2. Portfolio Analysis (Multiple Stocks)")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            return analyze_single_stock()
        elif choice == "2":
            return analyze_portfolio()
        else:
            print("Error: Invalid choice. Please enter 1 or 2")
            return 1
    
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        logger.info("Analysis interrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n✗ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
