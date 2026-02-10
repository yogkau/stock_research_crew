from crewai import Agent, LLM
from crewai_tools import SerperDevTool
from perf import TimingLLM, CachingLLM

search_tool = SerperDevTool()

_base_llm = LLM(
    model="ollama/mistral",
    #model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.2
)

# Wrap base LLM with timing and caching to reduce repeated work and record durations
# TimingLLM records durations to .cache/profile.json
# CachingLLM stores per-prompt responses in .cache/cache.json
timed_llm = TimingLLM(_base_llm, model_name="ollama/mistral")
llm = CachingLLM(timed_llm, model_name="ollama/mistral")

market_researcher = Agent(
    role="Market Research Analyst",
    goal="Research company background, sector, competitors, and recent developments",
    backstory="Expert in equity research and macro trends",
    tools=[search_tool],   # 🔥 Web search enabled
    llm=llm,
    verbose=False
)

technical_analyst = Agent(
    role="Fundamental Analyst",
    goal="Analyze business strength, valuation logic, and performance trends",
    backstory="Experienced analyst focused on fundamentals",
    llm=llm,
    verbose=False
)

risk_manager = Agent(
    role="Risk Assessment Analyst",
    goal="Identify key risks and downside scenarios",
    backstory="Risk-focused analyst protecting capital",
    llm=llm,
    verbose=False
)

decision_agent = Agent(
    role="Investment Decision Maker",
    goal="Provide a clear Buy, Hold, or Avoid decision with reasoning",
    backstory="Senior portfolio manager balancing growth and risk",
    llm=llm,
    verbose=False
)

scoring_agent = Agent(
    role="Stock Scoring & Allocation Analyst",
    goal="Assign a quantitative score and final investment decision",
    backstory=(
        "Senior investment committee member who converts qualitative "
        "analysis into structured scores and clear decisions"
    ),
    llm=llm,
    verbose=False
)
