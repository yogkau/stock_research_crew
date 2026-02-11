"""Portfolio analyzer for batch processing multiple stocks."""
import logging
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from stock_research_crew.crew import stock_crew
from stock_research_crew.portfolio_crew import create_portfolio_crew
from stock_research_crew.cache import cache_manager
from config import Config

logger = logging.getLogger(__name__)


class PortfolioAnalyzer:
    """Analyze multiple stocks and provide portfolio recommendations."""
    
    def __init__(self, stocks: List[str], portfolio_size: float = 100000):
        self.stocks = [s.strip().upper() for s in stocks]
        self.portfolio_size = portfolio_size
        self.individual_results = {}
    
    def analyze_single_stock(self, stock: str) -> Dict:
        """Analyze a single stock with caching."""
        try:
            # Check cache first
            cached = cache_manager.get_cached_result(stock)
            if cached:
                logger.info(f"Using cached result for {stock}")
                return {"stock": stock, "result": cached, "cached": True}
            
            # Run analysis
            logger.info(f"Analyzing {stock}...")
            result = stock_crew.kickoff(inputs={"stock": stock})
            output = str(result)
            
            # Save to cache
            cache_manager.save_result(stock, output)
            
            return {"stock": stock, "result": output, "cached": False}
            
        except Exception as e:
            logger.error(f"Failed to analyze {stock}: {e}")
            return {"stock": stock, "result": None, "error": str(e)}
    
    def analyze_all_stocks(self, parallel: bool = False) -> Dict[str, str]:
        """Analyze all stocks in the portfolio."""
        logger.info(f"Analyzing {len(self.stocks)} stocks...")
        
        if parallel and len(self.stocks) > 1:
            # Parallel processing
            with ThreadPoolExecutor(max_workers=min(3, len(self.stocks))) as executor:
                futures = {executor.submit(self.analyze_single_stock, stock): stock 
                          for stock in self.stocks}
                
                for future in as_completed(futures):
                    result = future.result()
                    if result.get("result"):
                        self.individual_results[result["stock"]] = result["result"]
        else:
            # Sequential processing
            for stock in self.stocks:
                result = self.analyze_single_stock(stock)
                if result.get("result"):
                    self.individual_results[result["stock"]] = result["result"]
        
        return self.individual_results
    
    def analyze_portfolio(self) -> str:
        """Perform portfolio-level analysis."""
        if not self.individual_results:
            raise ValueError("No individual stock results available. Run analyze_all_stocks() first.")
        
        logger.info("Performing portfolio-level analysis...")
        
        # Create portfolio crew with stock list
        portfolio_crew = create_portfolio_crew(list(self.individual_results.keys()), self.portfolio_size)
        
        # Prepare context with all individual analyses
        context = "\n\n".join([
            f"=== {stock} Analysis ===\n{result}"
            for stock, result in self.individual_results.items()
        ])
        
        # Run portfolio analysis
        portfolio_result = portfolio_crew.kickoff(inputs={
            "stocks": list(self.individual_results.keys()),
            "context": context
        })
        
        return str(portfolio_result)
    
    def generate_full_report(self, parallel: bool = False) -> Dict:
        """Generate complete portfolio report."""
        # Analyze individual stocks
        self.analyze_all_stocks(parallel=parallel)
        
        # Analyze portfolio
        portfolio_analysis = self.analyze_portfolio()
        
        return {
            "individual_analyses": self.individual_results,
            "portfolio_analysis": portfolio_analysis,
            "stocks": self.stocks,
            "portfolio_size": self.portfolio_size
        }
