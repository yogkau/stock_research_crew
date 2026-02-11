"""Improved agent definitions with better configuration and error handling."""
from crewai import Agent, LLM
from crewai_tools import SerperDevTool
from stock_research_crew.perf import TimingLLM, CachingLLM
from stock_research_crew.cache import cache_manager
from config import Config
import logging

logger = logging.getLogger(__name__)

# Initialize search tool with error handling
try:
    search_tool = SerperDevTool() if Config.SERPER_API_KEY else None
    if not search_tool:
        logger.warning("SerperDevTool not configured - web search disabled")
except Exception as e:
    logger.error(f"Failed to initialize search tool: {e}")
    search_tool = None

# Configure base LLM
try:
    _base_llm = LLM(
        model=Config.LLM_MODEL,
        base_url=Config.LLM_BASE_URL,
        temperature=Config.LLM_TEMPERATURE,
        timeout=Config.LLM_TIMEOUT
    )
    
    # Wrap with timing and caching
    timed_llm = TimingLLM(_base_llm, model_name=Config.LLM_MODEL)
    timed_llm.set_log_callback(cache_manager.log_profile)
    
    llm = CachingLLM(timed_llm, model_name=Config.LLM_MODEL, cache_manager=cache_manager)
    
except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")
    raise

# Define agents
market_researcher = Agent(
    role="Market Research Analyst",
    goal="Research company background, sector, competitors, and recent developments",
    backstory="Expert in equity research and macro trends with 10+ years experience",
    tools=[search_tool] if search_tool else [],
    llm=llm,
    verbose=False
)

# Fixed: Renamed from technical_analyst to fundamental_analyst
fundamental_analyst = Agent(
    role="Fundamental Analyst",
    goal="Analyze business strength, valuation logic, and performance trends",
    backstory="Experienced analyst focused on fundamentals, financial statements, and business models",
    llm=llm,
    verbose=False
)

risk_manager = Agent(
    role="Risk Assessment Analyst",
    goal="Identify key risks and downside scenarios",
    backstory="Risk-focused analyst with expertise in identifying threats to capital preservation",
    llm=llm,
    verbose=False
)

# Consolidated decision agent (combines decision + scoring)
investment_advisor = Agent(
    role="Senior Investment Advisor",
    goal="Provide comprehensive investment recommendation with quantitative scoring",
    backstory=(
        "Senior portfolio manager with 15+ years experience balancing growth and risk. "
        "Expert at synthesizing research into actionable investment decisions with clear scoring."
    ),
    llm=llm,
    verbose=False
)
