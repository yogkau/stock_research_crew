"""Portfolio-specific agents for multi-stock analysis."""
from crewai import Agent
from stock_research_crew.agents import llm

# Portfolio-level agent for comparative analysis
portfolio_analyst = Agent(
    role="Portfolio Analyst",
    goal="Analyze multiple stocks together, compare them, and provide portfolio-level recommendations",
    backstory=(
        "Senior portfolio strategist with 20+ years experience in asset allocation and diversification. "
        "Expert at comparing stocks, identifying correlations, and building balanced portfolios."
    ),
    llm=llm,
    verbose=False
)

# Diversification specialist
diversification_analyst = Agent(
    role="Diversification Specialist",
    goal="Assess portfolio diversification, sector exposure, and risk concentration",
    backstory=(
        "Risk management expert specializing in portfolio construction and diversification strategies. "
        "Skilled at identifying concentration risks and recommending optimal allocation."
    ),
    llm=llm,
    verbose=False
)
