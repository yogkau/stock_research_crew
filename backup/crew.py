from crewai import Crew
from tasks import (
    research_task,
    analysis_task,
    risk_task,
    decision_task,
    scoring_task
)
from stock_research_crew.backup.agents import (
    market_researcher,
    technical_analyst,
    risk_manager,
    decision_agent,
    scoring_agent
)

stock_crew = Crew(
    agents=[
        market_researcher,
        technical_analyst,
        risk_manager,
        decision_agent,
        scoring_agent
    ],
    tasks=[
        research_task,
        analysis_task,
        risk_task,
        decision_task,
        scoring_task
    ],
    verbose=True
)
