"""Portfolio crew for analyzing multiple stocks."""
from crewai import Crew
from stock_research_crew.agents import (
    market_researcher,
    fundamental_analyst,
    risk_manager,
    investment_advisor
)
from stock_research_crew.tasks import (
    research_task,
    analysis_task,
    risk_task,
    investment_decision_task
)
from stock_research_crew.portfolio_agents import portfolio_analyst, diversification_analyst
from stock_research_crew.portfolio_tasks import (
    create_portfolio_comparison_task,
    create_portfolio_allocation_task
)
from config import Config
import logging

logger = logging.getLogger(__name__)


def create_stock_crew_for_symbol(stock: str):
    """Create a crew for analyzing a single stock."""
    return Crew(
        agents=[
            market_researcher,
            fundamental_analyst,
            risk_manager,
            investment_advisor
        ],
        tasks=[
            research_task,
            analysis_task,
            risk_task,
            investment_decision_task
        ],
        verbose=False
    )


def create_portfolio_crew(stocks: list, portfolio_size: float = 100000):
    """Create a crew for portfolio-level analysis."""
    try:
        portfolio_crew = Crew(
            agents=[
                portfolio_analyst,
                diversification_analyst
            ],
            tasks=[
                create_portfolio_comparison_task(stocks),
                create_portfolio_allocation_task(stocks, portfolio_size)
            ],
            verbose=True
        )
        
        logger.info(f"Portfolio crew initialized for {len(stocks)} stocks")
        return portfolio_crew
        
    except Exception as e:
        logger.error(f"Failed to initialize portfolio crew: {e}")
        raise
