from crewai import Task
from agents import (
    market_researcher, 
    technical_analyst, 
    risk_manager, 
    decision_agent,
    scoring_agent
)

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


scoring_task = Task(
    description="""
    Using all prior analysis for {stock}, assign scores:

    - Business Quality (0–30)
    - Growth Potential (0–25)
    - Valuation Attractiveness (0–20)
    - Risk Profile (0–25)

    Then:
    - Calculate total score (0–100)
    - Map to decision:
        75–100 = BUY
        50–74  = HOLD
        0–49   = AVOID

    Output in this format:
    - Individual scores
    - Total score
    - Final decision
    - 3–5 bullet point justification
    """,
    expected_output="Numerical stock score and final decision",
    agent=scoring_agent
)
