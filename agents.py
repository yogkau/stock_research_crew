from crewai import Agent, LLM
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.2
)

market_researcher = Agent(
    role="Market Research Analyst",
    goal="Research company background, sector, competitors, and recent developments",
    backstory="Expert in equity research and macro trends",
    tools=[search_tool],   # 🔥 Web search enabled
    llm=llm,
    verbose=True
)

technical_analyst = Agent(
    role="Fundamental Analyst",
    goal="Analyze business strength, valuation logic, and performance trends",
    backstory="Experienced analyst focused on fundamentals",
    llm=llm,
    verbose=True
)

risk_manager = Agent(
    role="Risk Assessment Analyst",
    goal="Identify key risks and downside scenarios",
    backstory="Risk-focused analyst protecting capital",
    llm=llm,
    verbose=True
)

decision_agent = Agent(
    role="Investment Decision Maker",
    goal="Provide a clear Buy, Hold, or Avoid decision with reasoning",
    backstory="Senior portfolio manager balancing growth and risk",
    llm=llm,
    verbose=True
)
