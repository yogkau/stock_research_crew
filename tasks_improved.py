"""Improved task definitions with consolidated decision-making."""
from crewai import Task
from agents_improved import (
    market_researcher,
    fundamental_analyst,
    risk_manager,
    investment_advisor
)

research_task = Task(
    description="""
    Research the company {stock} comprehensively.
    
    Required information:
    - Company description and business model
    - Industry sector and market position
    - Key competitors and competitive advantages
    - Long-term growth drivers and catalysts
    - Recent news and developments (if search available)
    
    Be specific and factual. Cite sources when possible.
    """,
    expected_output="Detailed company and sector overview with competitive analysis",
    agent=market_researcher
)

analysis_task = Task(
    description="""
    Perform fundamental analysis of {stock}.
    
    Analyze:
    - Revenue and profit trends (qualitative assessment)
    - Business model strength and sustainability
    - Competitive moat and market position
    - Valuation assessment (overvalued/undervalued/fairly valued)
    - Key financial metrics and ratios (if available)
    
    Provide clear reasoning for all assessments.
    """,
    expected_output="Comprehensive fundamental analysis with valuation perspective",
    agent=fundamental_analyst
)

risk_task = Task(
    description="""
    Identify and assess all material risks for {stock}.
    
    Categories to cover:
    - Business risks (competition, disruption, execution)
    - Market risks (economic cycles, sector trends)
    - Financial risks (debt, cash flow, profitability)
    - Regulatory and legal risks
    - Management and governance risks
    
    Rate each risk as Low/Medium/High severity.
    """,
    expected_output="Structured risk analysis with severity ratings",
    agent=risk_manager
)

# Consolidated decision task (replaces separate decision + scoring tasks)
investment_decision_task = Task(
    description="""
    Synthesize all research, fundamental analysis, and risk assessment for {stock} 
    into a comprehensive investment recommendation.
    
    Provide:
    
    1. QUANTITATIVE SCORES (0-100 scale):
       - Business Quality (0-30): Management, moat, model strength
       - Growth Potential (0-25): Revenue growth, market expansion
       - Valuation (0-20): Price attractiveness vs intrinsic value
       - Risk Profile (0-25): Inverse of risk (higher = lower risk)
       - TOTAL SCORE (sum of above)
    
    2. INVESTMENT DECISION:
       - 75-100: BUY (Strong conviction)
       - 50-74: HOLD (Neutral/Wait)
       - 0-49: AVOID (High risk or overvalued)
    
    3. CONFIDENCE LEVEL: Low / Medium / High
    
    4. KEY REASONING (4-6 bullet points):
       - Main strengths supporting the decision
       - Main concerns or risks
       - Catalysts or triggers to watch
    
    Format output clearly with sections for scores, decision, confidence, and reasoning.
    """,
    expected_output="Complete investment recommendation with scores, decision, confidence, and detailed reasoning",
    agent=investment_advisor
)
