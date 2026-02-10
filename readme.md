📊 AI Stock Research Crew (Local & Free)

Overview

AI Stock Research Crew is a local, multi-agent system that simulates an equity research team. It uses CrewAI to orchestrate several specialized agents and runs fully locally with Ollama as the LLM runtime (no paid APIs required).

Quick highlights

- Runs 100% locally (Ollama + local LLM)
- No OpenAI or external paid APIs required
- Designed for learning multi-agent orchestration and building reproducible research workflows

Project objective

Given a stock name or ticker, the system produces a structured research report by:

- Researching the company and its market
- Producing a qualitative fundamental and technical analysis
- Identifying material risks
- Producing a final recommendation and numerical scoring

Important: This is educational research software, not financial advice.

Architecture (Agents & Flow)

The system currently uses five agents, each mapped to a specific task in the pipeline:

1. `market_researcher` — gathers company description, sector context, competitors, and long-term drivers.
2. `technical_analyst` — provides qualitative fundamental & technical commentary (revenue, margins, business strength).
3. `risk_manager` — enumerates business, market, financial, and regulatory risks.
4. `decision_agent` — synthesizes prior outputs and issues a recommendation (Buy / Hold / Avoid) with confidence and reasoning.
5. `scoring_agent` — assigns numerical scores (Business Quality, Growth, Valuation, Risk), computes the total (0–100), and maps that to the final decision.

Processing flow (high level)

1. `main.py` prompts for a stock ticker/name and calls `stock_crew.kickoff(inputs={'stock': ...})`.
2. `crew.py` instantiates a `Crew` with the ordered list of agents and tasks.
3. Crew runs the tasks in sequence: `research_task` → `analysis_task` → `risk_task` → `decision_task` → `scoring_task`.
4. Each `Task` (in `tasks.py`) runs with its assigned agent; agents are defined/configured in `agents.py`.
5. Final combined result (structured report + scores) is returned and printed by `main.py`.

Project structure (key files)

- `agents.py` — Agent definitions, role prompts, and LLM configuration.
- `tasks.py` — `Task` objects describing inputs/expected outputs for each agent.
- `crew.py` — Crew instantiation wiring agents and tasks together.
- `main.py` — CLI entry point that runs the crew and prints the final report.
- `requirements.txt` — Python dependencies.

Setup

1. Create a virtual environment and activate it (Windows example):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

3. Install Ollama (visit https://ollama.com/download) and pull a recommended model (example):

```powershell
# Example (adjust model name as needed)
ollama pull llama3.1
ollama run llama3.1
```

Running the project

```powershell
python main.py
```

Enter a stock name or ticker when prompted (for example: `Apple` or `AAPL`). The system will execute each agent in order and print a structured final report.

Example output (abbreviated)

## FINAL STOCK RESEARCH REPORT

Company overview: <company description & sector context>

Fundamental analysis: <qualitative revenue/profit/commentary>

Risk analysis: <enumerated risks & red flags>

Decision: BUY / HOLD / AVOID (with confidence level)

Scores:

- Business Quality: 24/30
- Growth Potential: 18/25
- Valuation: 14/20
- Risk Profile: 20/25
- Total: 76/100 → BUY

Notes on customization

- Tasks and agent prompts are in `tasks.py` and `agents.py` — edit them to change agent behavior or expected outputs.
- The `Crew` is configured in `crew.py`; reorder agents/tasks to change execution order.

Troubleshooting

- If Ollama or the chosen model is not installed, the LLM calls will fail — ensure `ollama` is available on PATH and the model is pulled.
- If you see authentication or network errors, confirm you're running fully local models or check the environment for any external API keys.

Contributing & Future work

- Add a web UI (Streamlit) for interactive use
- Integrate live web search or data sources (careful with external APIs)
- Add caching/memory and agent-to-agent long-term memory

License & Disclaimer

This repository is intended for education and research only. Not financial advice. Use at your own risk.

Author

Yogesh Kaushik

--
Updated README to reflect the current 5-agent pipeline and processing flow.
