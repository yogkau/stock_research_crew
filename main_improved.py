"""Improved main entry point with error handling and validation."""
import sys
import logging
from crew_improved import stock_crew
from cache_improved import cache_manager
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


def print_report(result: str):
    """Print formatted report."""
    print("\n" + "=" * 60)
    print("STOCK RESEARCH REPORT")
    print("=" * 60)
    print(result)
    print("=" * 60)


def main():
    """Main execution function."""
    try:
        # Get stock input
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
        print(f"  Cache expiry: {Config.CACHE_EXPIRY_HOURS} hours")
        print(f"  This may take several minutes...\n")
        
        try:
            result = stock_crew.kickoff(inputs={"stock": stock_name})
            output = str(result)
            
            # Save to cache
            cache_manager.save_result(stock_name, output)
            logger.info(f"Analysis completed and cached for {stock_name}")
            
            # Print result
            print_report(output)
            
            # Print performance summary
            print(f"\n✓ Analysis complete. Results cached for {Config.CACHE_EXPIRY_HOURS} hours.")
            print(f"  Performance logs: {Config.PROFILE_FILE}")
            
            return 0
            
        except Exception as e:
            logger.error(f"Crew execution failed: {e}", exc_info=True)
            print(f"\n✗ Error during analysis: {e}")
            print("  Check that Ollama is running and the model is available.")
            print(f"  Model: {Config.LLM_MODEL}")
            print(f"  Base URL: {Config.LLM_BASE_URL}")
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
