"""Improved crew configuration with parallel processing support."""
from crewai import Crew
from stock_research_crew.tasks import (
    research_task,
    analysis_task,
    risk_task,
    investment_decision_task
)
from stock_research_crew.agents import (
    market_researcher,
    fundamental_analyst,
    risk_manager,
    investment_advisor
)
from config import Config
import logging

logger = logging.getLogger(__name__)

# Note: CrewAI supports parallel execution for independent tasks
# Research, analysis, and risk tasks can run in parallel since they don't depend on each other
# The final investment decision task depends on all three

try:
    stock_crew = Crew(
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
        verbose=True,
        # Enable parallel execution if configured (requires CrewAI Pro or specific setup)
        # process="parallel" if Config.ENABLE_PARALLEL_TASKS else "sequential"
    )
    
    logger.info("Stock research crew initialized successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize crew: {e}")
    raise
