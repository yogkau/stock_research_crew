from crewai import Task
from agents import market_researcher, technical_analyst, risk_manager, decision_agent


research_task = Task(
    description="""
    Research the company {stock}.
    Include:
    - What the company does
    - Industry & competitors
    - Long-term growth drivers
    """,
    expected_output="Company and sector overview",
    agent=market_researcher
)

analysis_task = Task(
    description="""
    Analyze {stock} fundamentals:
    - Revenue & profit trend (qualitative)
    - Valuation logic (over/under valued)
    - Business strength
    """,
    expected_output="Fundamental analysis summary",
    agent=technical_analyst
)

risk_task = Task(
    description="""
    Identify risks for {stock}:
    - Business risks
    - Market risks
    - Financial or regulatory risks
    """,
    expected_output="Risk analysis",
    agent=risk_manager
)

decision_task = Task(
    description="""
    Based on the research, analysis, and risk assessment for {stock},
    provide:
    - Final recommendation: Buy / Hold / Avoid
    - Confidence level (Low / Medium / High)
    - Clear reasoning in bullet points
    """,
    expected_output="Final investment decision with justification",
    agent=decision_agent
)
