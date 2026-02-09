📊 AI Stock Research Crew (Local & Free)
Overview

AI Stock Research Crew is a fully local, multi-agent AI system built using CrewAI and Ollama.
It simulates how a real equity research team works by assigning specialized AI agents to collaborate on stock analysis.

✅ Runs 100% locally
✅ No OpenAI / no paid APIs
✅ Ideal for learning AI agents & orchestration
✅ Portfolio-ready project

🎯 Project Objective

    Given a stock name or ticker, the system produces a structured research report by:

    Researching the company and its sector

    Analyzing fundamentals and business strength

    Identifying key risks and downside scenarios

⚠️ This project is for education and research only, not financial advice.

🧠 Architecture (Multi-Agent Design)

The project uses three AI agents, each with a clear responsibility:

1️⃣ Market Research Analyst

    Understands what the company does

    Identifies industry position & competitors

    Highlights long-term growth drivers

2️⃣ Fundamental & Technical Analyst

    Evaluates business quality

    Analyzes revenue, profitability trends (qualitative)

    Assesses valuation logic (over/under valued)

3️⃣ Risk Assessment Analyst

    Identifies business, financial, and market risks

    Highlights red flags and downside scenarios

    Focuses on capital protection

    Each agent works independently, and CrewAI orchestrates their collaboration.

🧰 Tech Stack

    Python 3.10+
    CrewAI – Multi-agent orchestration
    LiteLLM – LLM abstraction layer
    Ollama – Local LLM runtime
    Llama 3.1 (8B) – Primary language model

🗂 Project Structure
ai_stock_crew/
│
├── agents.py # Agent definitions (roles, goals, LLM config)
├── tasks.py # Tasks assigned to each agent
├── crew.py # Crew orchestration
├── main.py # Entry point
├── requirements.txt
└── README.md

⚙️ Setup Instructions
1️⃣ Create & Activate Virtual Environment
python -m venv crewai-env
crewai-env\Scripts\activate

2️⃣ Install Dependencies
pip install crewai crewai-tools litellm requests
3️⃣ Install Ollama

Download from:
👉 https://ollama.com/download

Pull recommended model:
ollama pull llama3.1

Verify:
ollama run llama3.1

▶️ How to Run the Project
python main.py

When prompted:
Enter stock name or ticker: Apple

The system will:
Execute each agent step-by-step
Print a structured stock research report

🧪 Example Output (High-Level)
Company Overview:
Apple is a global consumer technology company...

Fundamental Analysis:
Strong brand, high margins, premium valuation...

Risk Assessment:
Revenue concentration in iPhone, regulatory risks...

💡 Key Learning Outcomes

    By building this project, you learn:

    How to design AI agents with roles & goals

    How multi-agent collaboration works

    How to run LLMs locally using Ollama

    How CrewAI orchestrates task execution

    How to scale from simple prompts to agent systems

🚀 Future Enhancements (Planned)

    Buy / Hold / Avoid scoring system

    Web search tool for real-time context

    Portfolio-level analysis

    Streamlit UI

    Technical indicators integration

    Agent memory & caching

🔒 Disclaimer

This project is for educational purposes only.
It does not provide investment advice or real-time financial data.

🧭 Author - Yogesh Kaushik

Built as a hands-on learning project for AI Agents & Autonomous Systems using CrewAI.
