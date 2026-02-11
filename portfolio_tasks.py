"""Portfolio-specific tasks for multi-stock analysis."""
from crewai import Task
from stock_research_crew.portfolio_agents import portfolio_analyst, diversification_analyst

def create_portfolio_comparison_task(stocks: list):
    """Create task to compare multiple stocks."""
    stock_list = ", ".join(stocks)
    
    return Task(
        description=f"""
        Compare and analyze the following stocks: {stock_list}
        
        For each stock, review the individual analysis and provide:
        
        1. COMPARATIVE ANALYSIS:
           - Rank stocks by overall score (highest to lowest)
           - Compare business quality across stocks
           - Compare growth potential across stocks
           - Compare valuation attractiveness
           - Compare risk profiles
        
        2. SECTOR & CORRELATION:
           - Identify sector distribution
           - Note any sector concentration
           - Identify potential correlations between stocks
        
        3. STRENGTHS & WEAKNESSES:
           - Best stock for growth
           - Best stock for stability
           - Best stock for value
           - Highest risk stock
           - Most balanced stock
        
        4. PORTFOLIO INSIGHTS:
           - Which stocks complement each other
           - Which stocks are redundant
           - Recommended core holdings vs satellite positions
        
        Present findings in a clear, structured format.
        """,
        expected_output="Comparative analysis of all stocks with rankings and portfolio insights",
        agent=portfolio_analyst
    )


def create_portfolio_allocation_task(stocks: list, portfolio_size: float = 100000):
    """Create task to recommend portfolio allocation."""
    stock_list = ", ".join(stocks)
    
    return Task(
        description=f"""
        Based on the comparative analysis of: {stock_list}
        
        Provide portfolio allocation recommendations for a ${portfolio_size:,.0f} portfolio:
        
        1. RECOMMENDED ALLOCATION:
           - Percentage allocation for each stock
           - Dollar amount for each position
           - Rationale for each allocation
        
        2. DIVERSIFICATION ASSESSMENT:
           - Sector diversification score (0-100)
           - Risk diversification score (0-100)
           - Overall portfolio balance rating
        
        3. PORTFOLIO STRATEGY:
           - Core holdings (largest positions)
           - Satellite holdings (smaller positions)
           - Stocks to exclude (if any) and why
        
        4. RISK MANAGEMENT:
           - Overall portfolio risk level (Low/Medium/High)
           - Concentration risks to watch
           - Rebalancing triggers
        
        5. FINAL RECOMMENDATION:
           - Is this a well-balanced portfolio? (Yes/No)
           - Key strengths of the portfolio
           - Key weaknesses or gaps
           - Suggested improvements
        
        Format as a clear portfolio allocation table with percentages and amounts.
        """,
        expected_output="Detailed portfolio allocation with percentages, amounts, and diversification analysis",
        agent=diversification_analyst
    )
